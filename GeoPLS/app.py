import streamlit as st
import streamlit.components.v1 as components
import json
import datetime  # Required for capturing submission timestamp

# I have extracted the key from the full URL you provided.
# NOTE: This key is now only used for the Google Maps URL link button,
# as the interactive map component below now uses a keyless CDN based on your request.
GOOGLE_MAPS_API_KEY = "AIzaSyAOVYRIgupAurZup5y1PRh8Ismb1A3lLao"

# --- 0. Session State Initialization (Moved to Top for Robustness) ---
# Initialize state for map center (defaulted to a general area)
if 'map_center_lat' not in st.session_state:
    st.session_state.map_center_lat = 30.0
if 'map_center_lon' not in st.session_state:
    st.session_state.map_center_lon = 15.0
# Initialize state for employee details and photo
if 'employee_name' not in st.session_state:
    st.session_state.employee_name = ""
if 'employee_id' not in st.session_state:
    st.session_state.employee_id = ""
if 'selfie_image' not in st.session_state:
    st.session_state.selfie_image = None  # To hold the file upload object from st.camera_input
if 'submission_data' not in st.session_state:
    st.session_state.submission_data = None  # Holds the last successful check-in data

# --- 1. Custom JavaScript/HTML Component Code for GPS Button (Existing) ---

GPS_COMPONENT = """
<!DOCTYPE html>
<html>
<head>
    <title>GPS Finder</title>
    <style>
        body { margin: 0; padding: 0; font-family: sans-serif; }
        .container { text-align: center; padding: 10px; }
        #getLocationButton {
            background-color: #4f46e5;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.15s ease-in-out;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        #getLocationButton:hover {
            background-color: #4338ca;
        }
        .icon { margin-right: 8px; font-size: 1.2em; }
        #js-results-gps {
            text-align: left; 
            margin-top: 10px; 
            border: 1px solid #d1d5db; 
            background-color: #f9fafb;
            padding: 10px; 
            border-radius: 6px; 
            font-size: 0.9em;
            color: #374151;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <div id="js-results-gps" style="display: none;">
            <p style="margin: 0;">
                **Latitude:** <span id="js-lat-output" style="font-weight: bold; color: #1e40af;">--</span>
            </p>
            <p style="margin: 0;">
                **Longitude:** <span id="js-lon-output" style="font-weight: bold; color: #1e40af;">--</span>
            </p>
        </div>

        <button id="getLocationButton" 
                onclick="getAccurateLocation()">
            <span id="button-icon" class="icon">📍</span> Find My Exact Location
        </button>
        <p id="status-message" style="margin-top: 15px; text-align: center; color: #4b5563;">
            Click the button to request location.
        </p>
    </div>

    <script>
        const statusEl = document.getElementById('status-message');
        const buttonEl = document.getElementById('getLocationButton');
        const buttonIconEl = document.getElementById('button-icon');
        const jsResultsEl = document.getElementById('js-results-gps');
        const jsLatOutputEl = document.getElementById('js-lat-output');
        const jsLonOutputEl = document.getElementById('js-lon-output');

        // Function to send data back to Streamlit
        function sendToStreamlit(data) {
            window.parent.postMessage({
                source: 'streamlit',
                type: 'streamlit:setComponentValue',
                value: data,
            }, '*');
        }

        // --- Success Callback (sends data back) ---
        function success(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            const accuracy = position.coords.accuracy;

            // Update and show Lat/Lon in the HTML component immediately
            jsLatOutputEl.innerText = latitude.toFixed(6);
            jsLonOutputEl.innerText = longitude.toFixed(6);
            jsResultsEl.style.display = 'block';

            statusEl.innerText = `Location found! Accuracy: ${accuracy.toFixed(2)}m`;
            buttonEl.style.backgroundColor = '#10b981'; // Green on success
            buttonEl.innerText = 'Location Found!';
            buttonIconEl.innerText = '✅';

            // Send Lat, Lon, and Accuracy back to Streamlit Python backend
            sendToStreamlit({ 
                lat: latitude, 
                lon: longitude, 
                accuracy: accuracy 
            });
        }

        // --- Error Callback (sends error back) ---
        function error(err) {
            let message = '';
            let icon = '❌';
            jsResultsEl.style.display = 'none'; // Hide results on error

            switch(err.code) {
                case err.PERMISSION_DENIED:
                    message = "ACCESS_DENIED";
                    statusEl.innerText = "❌ Permission Denied. Please grant access and retry.";
                    break;
                case err.POSITION_UNAVAILABLE:
                    message = "UNAVAILABLE";
                    statusEl.innerText = "❌ Location unavailable.";
                    break;
                case err.TIMEOUT:
                    message = "TIMEOUT";
                    statusEl.innerText = "❌ Request timed out.";
                    break;
                default:
                    message = "UNKNOWN_ERROR";
                    statusEl.innerText = `❌ Error: ${err.message}`;
            }
            buttonEl.style.backgroundColor = '#ef4444'; // Red on error
            buttonEl.innerText = 'Location Error';
            buttonIconEl.innerText = icon;

            // Send error signal back to Streamlit Python backend
            sendToStreamlit({ error: message });
        }

        // --- Main Geolocation Function ---
        window.getAccurateLocation = function() {
            if (!navigator.geolocation) {
                statusEl.innerText = 'Geolocation not supported by this browser.';
                sendToStreamlit({ error: 'NOT_SUPPORTED' });
                return;
            }

            // Reset UI state before starting lookup
            jsResultsEl.style.display = 'none';
            statusEl.innerText = 'Requesting location... (Check for pop-up)';
            buttonEl.innerHTML = '<span class="icon">⏳</span> Finding Location...';
            buttonEl.style.backgroundColor = '#f59e0b'; // Amber while loading

            const options = {
                enableHighAccuracy: true,
                timeout: 15000, 
                // FIX: Allow caching for 60 seconds (60000ms) to prevent repetitive permission requests on mobile.
                maximumAge: 60000 
            };

            navigator.geolocation.getCurrentPosition(success, error, options);
        }

    </script>
</body>
</html>
"""

# --- 2. Custom JavaScript/HTML Component Code for Interactive Map (Existing) ---

# This template accepts dynamic initial lat/lon via .format() and uses the user's keyless map configuration.
MAP_CLICK_COMPONENT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Map</title>
    <meta name="viewport" content="initial-scale=1.0">
    <meta charset="utf-8">
    <style>
        /* Streamlit Wrapper for sizing and aesthetics */
        #map-container {{ 
            height: 500px; 
            width: 100%;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        /* Map Element (from user's request) */
        #map {{
            height: 100%;
        }}
        /* Optional: Makes the sample page fill the window. */
        html, body {{
            height: 100%;
            margin: 0;
            padding: 0;
        }}
    </style>
</head>
<body>
    <div id="map-container">
        <div id="map"></div>
    </div>

    <script>
        // Values injected from Streamlit Python state
        const INITIAL_LAT = {initial_lat};
        const INITIAL_LON = {initial_lon};

        var map; // Global map variable
        var marker; // Global marker variable

        function initMap() {{
            const default_lat = 30.0;
            const default_lon = 15.0;

            const center_coords = {{ lat: INITIAL_LAT, lng: INITIAL_LON }};
            // Set zoom level: close zoom (14) if custom coordinates are provided, wide zoom (2) otherwise.
            const initial_zoom = (INITIAL_LAT !== default_lat || INITIAL_LON !== default_lon) ? 14 : 2; 

            map = new google.maps.Map(document.getElementById('map'), {{
                center: center_coords, // Use dynamic center based on GPS result
                zoom: initial_zoom
            }});

            // Place marker at the captured GPS location for verification
            if (INITIAL_LAT !== default_lat || INITIAL_LON !== default_lon) {{
                marker = new google.maps.Marker({{
                    position: center_coords,
                    map: map,
                    title: "Captured GPS Location"
                }});
            }}
        }}
    </script>
    <script src="https://cdn.jsdelivr.net/gh/somanchiu/Keyless-Google-Maps-API@v7.1/mapsJavaScriptAPI.js"
    async defer></script>
</body>
</html>
"""

# --- 3. Streamlit Application (Python) ---

st.set_page_config(page_title="RD Corp Personnel Location Slip", layout="centered")

st.title("RD Corp Personnel Location Slip")
st.markdown("This system help personnel to record location throgh mobile devices.")

# Use a form to group all input elements for a single submission
with st.form(key="employee_checkin_form"):
    st.header("Employee Information")

    # 1. Employee Details Input
    col_name, col_id = st.columns(2)
    with col_name:
        st.session_state.employee_name = st.text_input(
            "Employee Name",
            value=st.session_state.employee_name or "Jane Doe"
        )
    with col_id:
        st.session_state.employee_id = st.text_input(
            "Employee ID",
            value=st.session_state.employee_id or "E12345"
        )

    st.markdown("---")

    # 2. Selfie Camera Input (MODIFIED)
    st.subheader("1. Take a Selfie")

    # Use an expander to house the camera input. The user clicks the expander
    # (which acts like a 'Open Camera' button) to activate the camera.
    with st.expander("📸 Click to Open Camera"):
        # Streamlit's built-in camera input is perfect for phone selfie capture
        captured_selfie = st.camera_input("Capture Selfie")

        # Update the session state with the captured photo object
        if captured_selfie:
            st.session_state.selfie_image = captured_selfie
            st.success("Selfie captured!")

    # Display status outside the expander
    if st.session_state.selfie_image:
        st.info("Selfie is ready for submission.")
    else:
        st.warning("Please click **'Click to Open Camera'** and take a selfie.")

    st.markdown("---")

    # 3. GPS Location Capture (Existing)
    st.subheader("2. Capture Current Location")
    st.caption("Press the button below to get the precise location of your device.")

    # Embed the GPS button component
    gps_location_result = components.html(
        GPS_COMPONENT,
        height=200,
        scrolling=False,
    )

    # Process GPS Button Results (updates map center state for the form)
    if isinstance(gps_location_result, dict):

        # Check for successful location capture (it will have 'lat' and 'lon' keys)
        if 'lat' in gps_location_result and 'lon' in gps_location_result:

            lat = gps_location_result['lat']
            lon = gps_location_result['lon']
            # Safely get accuracy, defaulting to 0.0 if key is missing
            accuracy = gps_location_result.get('accuracy', 0.0)

            st.success(f"✅ GPS Location captured: {lat:.6f}, {lon:.6f} (Accuracy: {accuracy:.2f} m)")
            # Update map center state (used for verification map and final submission)
            st.session_state.map_center_lat = lat
            st.session_state.map_center_lon = lon

        # Check for error code if the 'lat' and 'lon' keys were not found
        elif 'error' in gps_location_result:
            error_code = gps_location_result['error']
            error_map = {
                "ACCESS_DENIED": "Permission denied. Check browser settings.",
                "UNAVAILABLE": "Location unavailable.",
                "TIMEOUT": "Request timed out.",
                "NOT_SUPPORTED": "Geolocation API not supported."
            }
            st.error(f"❌ GPS Error: {error_code} - {error_map.get(error_code, 'Unknown error')}")

        # Fallback for unexpected dictionary structure
        else:
            st.warning("⚠️ Received an unexpected result dictionary from the GPS component.")

    # Display current location status
    if st.session_state.map_center_lat != 30.0 or st.session_state.map_center_lon != 15.0:
        st.info(
            f"Current Check-in Location: Lat {st.session_state.map_center_lat:.6f}, Lon {st.session_state.map_center_lon:.6f}")
    else:
        st.warning("Please click the **'Find My Exact Location'** button to record your current location.")

    st.markdown("---")

    # The submit button for the form
    submit_button = st.form_submit_button(label="Save Record")

# --- Form Submission Logic ---
if submit_button:
    # 1. Validation
    if not st.session_state.employee_name or not st.session_state.employee_id:
        st.error("Submission Failed: Please enter **Employee Name** and **ID**.")
    elif st.session_state.map_center_lat == 30.0 and st.session_state.map_center_lon == 15.0:
        st.error("Submission Failed: Please **capture your location**.")
    elif st.session_state.selfie_image is None:
        st.error("Submission Failed: Please **take a selfie** using the camera.")
    else:
        # 2. Collect Data
        submission_data = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": st.session_state.employee_name,
            "id": st.session_state.employee_id,
            "location_lat": st.session_state.map_center_lat,
            "location_lon": st.session_state.map_center_lon,
            "photo_status": "Captured",
        }

        # 3. Store submission data in state
        st.session_state.submission_data = submission_data
        st.success("✅ Record Saved Successfully!")
        # Rerun to clear the form and update the display
        st.rerun()

# --- 4. Location Verification Map ---
st.header("3. Location Verification Map")
st.markdown("The map below shows the current location.")

# Embed the interactive map component, centered on the last captured GPS location
map_click_result = components.html(
    MAP_CLICK_COMPONENT_TEMPLATE.format(
        initial_lat=st.session_state.map_center_lat,
        initial_lon=st.session_state.map_center_lon
    ),
    height=500,
    scrolling=False,
)

# --- 5. Display Last Successful Submission ---
if st.session_state.submission_data:
    st.header("Last Check-in Record")
    st.info(
        "NOTE: In a real application, this data (and the image file) would be saved to a database (like Firestore) or file storage.")

    # Display details
    data = st.session_state.submission_data

    col_a, col_b = st.columns(2)
    col_a.metric("Employee Name", data['name'])
    col_b.metric("Employee ID", data['id'])

    col_c, col_d = st.columns(2)
    col_c.metric("Location Latitude", f"{data['location_lat']:.6f}")
    col_d.metric("Location Longitude", f"{data['location_lon']:.6f}")

    st.metric("Timestamp", data['timestamp'])

    if st.session_state.selfie_image:
        st.subheader("Captured Selfie Photo")
        # To display an image captured by st.camera_input, you must first rewind the file object.
        st.session_state.selfie_image.seek(0)
        st.image(st.session_state.selfie_image, caption=f"Selfie for {data['name']}", use_column_width=True)
    else:
        st.warning("No selfie photo was available.")