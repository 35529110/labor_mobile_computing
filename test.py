import folium

coords = list()
with open("daten/signal-2024-02-07-mt.csv") as f:
    for line in f.readlines():
        line = line.split(',')
        x = line[0]
        y = line[1]
        point = (x,y)
        coords.append(point)

# Create a map centered around the first coordinate
m = folium.Map(location=coords[0], zoom_start=12)

# Add markers for each coordinate
for coord in coords:
    folium.Marker(location=coord).add_to(m)

# Save the map to an HTML file
m.save('map_with_markers.html')
