import pandas as pd
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

# Coordinates of the University of Kassel (to be filled with the correct values)
uni_kassel_coords = (9.473649508636461, 51.311156888467046) # Longitude, Latitude

cell_towers_df = pd.read_csv('daten/262.csv')

# Adding a new column 'distance_to_uni' to the dataframe
cell_towers_df['distance_to_uni'] = cell_towers_df.apply(lambda row: haversine(uni_kassel_coords[0], uni_kassel_coords[1], row[6], row[7]), axis=1)

# Filter out all towers that are more than 1km away
nearby_towers_df = cell_towers_df[cell_towers_df['distance_to_uni'] <= 1]

import folium

# Create a map centered around the University of Kassel
map_kassel = folium.Map(location=[uni_kassel_coords[1], uni_kassel_coords[0]], zoom_start=15)

# Add a marker for the University of Kassel
folium.Marker(
    [uni_kassel_coords[1], uni_kassel_coords[0]],
    popup='University of Kassel',
    icon=folium.Icon(color='red')
).add_to(map_kassel)

# Add markers for nearby cell towers
counter = 0
for index, row in nearby_towers_df.iterrows():
    folium.Marker(
        [row[7], row[6]],
        popup=f'Tower ID: {row[4]}',
        icon=folium.Icon(color='blue')
    ).add_to(map_kassel)
    counter += 1

print(f"number of towers: {counter}")

# Save the map to an HTML file
map_file_path = 'nearytowers1km.html'
map_kassel.save(map_file_path)
map_file_path
