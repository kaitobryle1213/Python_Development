import json
import urllib.request
import os
import sys

BASE_URL = "https://psgc.gitlab.io/api"
OUTPUT_FILE = os.path.join("RDRealty_App", "static", "data", "ph_location.json")

def fetch_json(endpoint):
    url = f"{BASE_URL}/{endpoint}/"
    print(f"Fetching {url}...")
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

def main():
    print("Starting data fetch...")
    
    # 1. Fetch all data
    provinces = fetch_json("provinces")
    cities_munis = fetch_json("cities-municipalities")
    barangays = fetch_json("barangays")

    print(f"Fetched {len(provinces)} provinces")
    print(f"Fetched {len(cities_munis)} cities/municipalities")
    print(f"Fetched {len(barangays)} barangays")

    # 2. Build Hierarchy
    # Create dictionaries for quick lookup
    # Province Code -> Province Object
    province_map = {p['code']: p for p in provinces}
    for p in provinces:
        p['cities'] = []

    # City/Muni Code -> City/Muni Object
    city_map = {}
    for c in cities_munis:
        city_map[c['code']] = c
        c['barangays'] = []
        
        # Add to province
        prov_code = c.get('provinceCode')
        if prov_code and prov_code in province_map:
            province_map[prov_code]['cities'].append(c)
        elif prov_code:
            pass

    # 3. Add Barangays to Cities
    for b in barangays:
        # Check cityCode or municipalityCode
        parent_code = b.get('cityCode') or b.get('municipalityCode')
        if parent_code and parent_code in city_map:
            city_map[parent_code]['barangays'].append(b)

    # 4. Handle NCR and unlinked cities
    orphan_cities = [c for c in cities_munis if not c.get('provinceCode')]
    ncr_cities = [c for c in orphan_cities if c.get('regionCode') == '130000000']
    
    if ncr_cities:
        ncr_container = next((p for p in provinces if p['name'] == 'Metro Manila'), None)
        if not ncr_container:
            ncr_container = {
                "code": "NCR",
                "name": "Metro Manila",
                "regionCode": "130000000",
                "cities": []
            }
            provinces.append(ncr_container)
            
        for c in ncr_cities:
            # Avoid duplicates if logic runs twice (unlikely here)
            if c not in ncr_container['cities']:
                ncr_container['cities'].append(c)
            
    # Sort everything
    provinces.sort(key=lambda x: x['name'])
    for p in provinces:
        p['cities'].sort(key=lambda x: x['name'])
        for c in p['cities']:
            c['barangays'].sort(key=lambda x: x['name'])

    # 5. Save
    output_data = {"provinces": provinces}
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
