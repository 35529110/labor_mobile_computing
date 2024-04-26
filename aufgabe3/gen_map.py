import folium

# Define a function to create a folium map
import pandas as pd





def create_map(data, map_title="Cell Towers Map"):
    # Initialize a map centered around Kassel
    map = folium.Map(location=[51.312711, 9.479746], zoom_start=12, tiles='Esri.WorldImagery')

    for point in data:
        point = point.strip().split(',')
        l_x, l_y = point[2].strip(), point[3].strip()
        # Only add a line if the station has valid coordinates
        if l_x != '?' and l_y != '?':
    
            # Add points to the map
            towers_found = 0
            try:
                latitude = float(l_y)
                longitude = float(l_x)
                folium.Marker([latitude, longitude], popup=f"ID: {data[1]}").add_to(map)
                towers_found += 1
            except ValueError as e:
                # Skip rows with invalid numeric data
                print(e)
                continue

    # Return the map object
    print(towers_found)
    return map

# Create maps for both datasets
with open('daten/locations_ot.csv') as locations_ot:
    map_ot = create_map(locations_ot.readlines(), "OT Cell Towers around Kassel")
    map_ot.save('aufgabe3/map_ot.html')

with open('daten/locations_mt.csv') as locations_mt:
    map_mt = create_map(locations_mt.readlines(), "MT Cell Towers around Kassel")
    map_mt.save('aufgabe3/map_mt.html')

