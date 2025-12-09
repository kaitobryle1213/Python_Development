import streamlit as st
import pandas as pd
import random
import time
import base64
from pathlib import Path

# Define the base directory (where app.py is located)
BASE_DIR = Path(__file__).parent.resolve()

def get_abs_path(filename: str) -> str:
    """Returns the absolute path for a file assumed to be in the same directory as app.py."""
    return str(BASE_DIR / filename)

# ----------------------------------------------------------------------
# --- BASE64 FUNCTIONS FOR RELIABLE BACKGROUND IMAGE INJECTION ---
# ----------------------------------------------------------------------

def get_img_as_base64(file_path):
    """Reads a file and returns its content as a base64 encoded string."""
    try:
        path_obj = Path(file_path)
        if not path_obj.is_file():
            # In deployment, Streamlit redacts errors, but this helps debug locally
            st.error(f"Image not found or is not a file at: {file_path}")
            return None

        with open(path_obj, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception as e:
        st.error(f"Error reading image file: {e}")
        return None


def set_background_base64(image_file):
    """Injects CSS to set the background image and ensures all content blocks
       are set to fully opaque white."""

    # 1. Determine the correct path to the image using the helper function
    image_path = get_abs_path(image_file) 
    
    # 2. Convert the image to Base64
    base64_img = get_img_as_base64(image_path)

    if base64_img:
        # 3. Inject the CSS using the Base64 data URI
        st.markdown(
            f"""
            <style>
            /* 1. Set the fixed background image for the entire app */
            .stApp {{
                background-image: url("data:image/png;base64,{base64_img}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed; 
                background-position: center;
                font-family: "Segoe UI", "Roboto", "Helvetica Neue", Arial, sans-serif;
            }}

            /* 2. CRITICAL FIX: Target the primary main content blocks for full opacity */
            .main > div,
            section.main, 
            div[data-testid="stAppViewBlock"],
            div[data-testid="stVerticalBlock"] > div:first-child,
            div[data-testid="stHorizontalBlock"] > div:first-child,
            [data-testid="stSidebar"],
            .stDataFrame,
            .block-container {{
                background-color: rgb(255, 255, 255) !important;
            }}

            /* Apply custom styling to the main content wrapper */
            .main > div {{
                padding: 15px; 
                border-radius: 10px;
            }}

            /* Ensure columns are also opaque (if you use columns) */
            [data-testid="column"] > div {{
                background-color: rgb(255, 255, 255) !important;
            }}

            </style>
            """,
            unsafe_allow_html=True
        )


# ----------------------------------------------------------------------
# --- Core Logic Functions (Roulette Functionality) ---
# ----------------------------------------------------------------------

def initialize_session_state():
    """Initializes all necessary session state variables for persistence across reruns."""
    if 'original_roster' not in st.session_state:
        st.session_state['original_roster'] = []

    if 'available_roster' not in st.session_state:
        st.session_state['available_roster'] = []

    if 'past_winners' not in st.session_state:
        st.session_state['past_winners'] = []

    if 'current_winner' not in st.session_state:
        st.session_state['current_winner'] = "Ready to spin!"

    if 'show_load_success_message' not in st.session_state:
        st.session_state['show_load_success_message'] = False

    if 'winner_placeholder' not in st.session_state:
        st.session_state['winner_placeholder'] = None


def load_data(uploaded_file):
    """Reads Excel data and returns a list of cleaned, unique names."""
    try:
        df = pd.read_excel(uploaded_file)
        if df.empty:
            st.error("The uploaded file is empty.")
            return []

        # Assuming the first column contains the names
        name_column = df.columns[0]

        # Clean data reliably: strip whitespace, remove duplicates
        employee_list = [
            name.strip() for name in df[name_column]
            .dropna()
            .astype(str)
            .drop_duplicates()
            .tolist()
        ]

        return employee_list

    except Exception as e:
        st.error(f"❌ Error loading file: Details: {e}")
        return []


def get_winner_html(name):
    """Generates the custom HTML for the winner display."""
    return f"""
        <div style='text-align: center; padding: 25px; border: 4px solid #ff4b4b; border-radius: 12px; background-color: #ffeded;'>
            <p style='font-size: 36px; color: #ff4b4b; margin: 3px 0;'></p>
            <h1 style='font-size: 56px; margin: 5px 0 0 0;'>{name.upper()}</h1>
        </div>
    """


def display_initial_winner_status(placeholder, message):
    """Displays the non-winner messages (Ready to spin, etc.)."""
    placeholder.info(message)


def spin_roulette():
    """Selects a random winner, removes them from the available list, and updates the history with a visual spin effect."""

    available_list = st.session_state['available_roster']
    placeholder = st.session_state['winner_placeholder']

    if not available_list:
        st.error("⚠️ No names left to spin! Click 'Reset Roster' to start over.")
        st.session_state['current_winner'] = "NO NAMES LEFT"
        display_initial_winner_status(placeholder, st.session_state['current_winner'])
        return

    # 1. Select the final winner
    winner = random.choice(available_list)

    # --- VISUAL SPINNING EFFECT IMPLEMENTATION ---

    spin_names = available_list * 5
    random.shuffle(spin_names)
    spin_names.extend([winner] * 5)

    delay = 0.05
    max_duration = 8.0
    start_time = time.time()

    for i, name in enumerate(spin_names):

        if time.time() - start_time > max_duration:
            break

        # Display the spinning name
        placeholder.markdown(get_winner_html(name), unsafe_allow_html=True)

        elapsed_percentage = (time.time() - start_time) / max_duration

        # Gradually slow down the spin by increasing the delay
        if elapsed_percentage < 0.5:
            delay *= 1.02
        elif elapsed_percentage < 0.8:
            delay *= 1.05
        else:
            delay *= 1.15
            if delay > 0.4:
                delay = 0.4

        time.sleep(delay)

    # Final display of the winner
    placeholder.markdown(get_winner_html(winner), unsafe_allow_html=True)

    # 3. Update the session state variables
    try:
        st.session_state['available_roster'].remove(winner)
        st.session_state['past_winners'].append(winner)
        st.session_state['current_winner'] = winner

        st.balloons()
        st.toast(f"🎉 Congratulations to {winner}!", icon="✅")

    except ValueError:
        st.error(f"Internal Error: Could not remove '{winner}' from the available list.")


def reset_roster():
    """Resets the available roster to the original list and clears the winners list."""
    st.session_state['original_roster'] = []
    st.session_state['available_roster'] = []
    st.session_state['past_winners'] = []
    st.session_state['current_winner'] = "Please upload a new roster to begin."
    st.toast("🔄 Roster cleared. Please upload a new file.")
    st.session_state['show_load_success_message'] = False
    st.rerun()


# ----------------------------------------------------------------------
# --- Streamlit UI Layout ---
# ----------------------------------------------------------------------

def main():
    # Set the custom background
    set_background_base64("background.png")

    # Set the page configuration, including the logo as the favicon
    st.set_page_config(
        page_title="RD Fishing X'Mas Party!",
        layout="centered",
        page_icon=get_abs_path("rd_fishing_logo.jpg") # <-- PATH FIX APPLIED
    )

    initialize_session_state()

    # ------------------------------------------------------------------
    # --- LOGO & TITLE SECTION (Centered and Larger Logo) ---
    # ------------------------------------------------------------------
    # Use a spacer column on the left to center the title block (0.1 + 2 + 7 = 9.1 total)
    col_spacer, col_logo, col_title = st.columns([0.1, 2, 7])

    # Display the logo in the small column
    with col_logo:
        # 🌟 ADJUSTED: Increased width for a bigger logo
        st.image(get_abs_path("rd_fishing_logo.jpg"), width=120) # <-- PATH FIX APPLIED

        # Display the title text in the large column
    with col_title:
        # 🌟 ADJUSTED: Added text-align: center to center the text in its column
        st.markdown(
            "<h1 style='display:inline-block; line-height: 1.1; text-align: left;'>RD Fishing Christmas Party!</h1>",
            unsafe_allow_html=True
        )
    # ------------------------------------------------------------------
    st.markdown("Once an employee is selected, they are **excluded** from future spins.")

    is_roster_loaded_flag = bool(st.session_state['original_roster'])

    # 1. Excel File Upload Section
    if not is_roster_loaded_flag:
        uploaded_file = st.file_uploader(
            "1. **Upload Employee Roster** (.xlsx)",
            type=['xlsx'],
            help="Upload a new file to load a new list."
        )

        if uploaded_file is not None:
            names = load_data(uploaded_file)

            if names:
                st.session_state['original_roster'] = names
                st.session_state['available_roster'] = names.copy()
                st.session_state['past_winners'] = []
                st.session_state['current_winner'] = "Roster loaded. Click 'Spin'!"
                st.session_state['show_load_success_message'] = True
                st.rerun()

    else:
        if st.session_state['show_load_success_message']:
            st.success(
                f"✅ Roster with **{len(st.session_state['original_roster'])}** employees is loaded. "
                "Click **'Reset Roster'** below to load a new file."
            )
            st.session_state['show_load_success_message'] = False

    st.markdown("---")

    # 2. Winner Display Setup
    st.subheader("🏆 Congratulations!")

    if st.session_state['winner_placeholder'] is None:
        st.session_state['winner_placeholder'] = st.empty()

    current_winner_text = st.session_state['current_winner']

    status_messages = ["Ready to spin!", "Roster loaded. Click 'Spin'!",
                       "Please upload a new roster to begin.", "NO NAMES LEFT"]

    if current_winner_text not in status_messages:
        st.session_state['winner_placeholder'].markdown(get_winner_html(current_winner_text), unsafe_allow_html=True)
    else:
        display_initial_winner_status(st.session_state['winner_placeholder'], current_winner_text)

    st.caption(f"")
    st.caption(f"")

    st.markdown("---")

    # 3. Control Panel (Spin and Reset Buttons)
    col1, col2 = st.columns([1, 1])

    is_roster_loaded = bool(st.session_state['available_roster'])

    with col1:
        if st.button(
                "🚀 **SPIN**",
                type="primary",
                use_container_width=True,
                disabled=not is_roster_loaded
        ):
            spin_roulette()

    with col2:
        if st.button("🔄 Reset", use_container_width=True, disabled=not is_roster_loaded_flag):
            reset_roster()

    st.markdown("---")

    # Optional: Display past winners list
    if st.session_state['past_winners']:
        st.subheader(f"Past Winners ({len(st.session_state['past_winners'])} of {len(st.session_state['original_roster'])})")
        st.dataframe(
            pd.DataFrame({'Winner': st.session_state['past_winners']}),
            use_container_width=True,
            hide_index=True
        )


if __name__ == "__main__":
    main()