import folium

# Define a function to create a folium map
import pandas as pd

# Load the data from the uploaded files
locations_ot = pd.read_csv('daten/locations_ot.csv')
locations_mt = pd.read_csv('daten/locations_mt.csv')

def create_map(data, map_title="Cell Towers Map"):
    # Initialize a map centered around Kassel
    map = folium.Map(location=[51.312711, 9.479746], zoom_start=12, tiles='Esri.WorldImagery')
    
    # Remove rows with invalid data
    valid_data = data.dropna().replace('?', pd.NA).dropna()  # Replace '?' with NA and then drop
    
    # Add points to the map
    for index, row in valid_data.iterrows():
        try:
            latitude = float(row[3])
            longitude = float(row[2])
            folium.Marker([latitude, longitude], popup=f"ID: {row[1]}").add_to(map)
        except ValueError:
            # Skip rows with invalid numeric data
            continue

    # Return the map object
    return map

# Create maps for both datasets
map_ot = create_map(locations_ot, "OT Cell Towers around Kassel")
map_mt = create_map(locations_mt, "MT Cell Towers around Kassel")

# Save maps to HTML files
map_ot.save('aufgabe3/map_ot.html')
map_mt.save('aufgabe3/map_mt.html')
