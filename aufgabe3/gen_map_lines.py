import folium
import os

files = filter(lambda s: s.startswith('signal'), os.listdir("daten"))



for file_name in files:
    lines = []  # Store lines between measurement points and LTE stations
    coords = list() 
    towers = set() # Use a set to avoid duplicate points

    # Open the measurement data file
    with open("daten/"+file_name) as f:
        if "-mt." in file_name:
            mode = "mt"
        else:
            mode = "ot"
        for line in f.readlines():
            parts = line.strip().split(',')
            # Check if the coordinate parts are valid numbers
            if parts[2].isdigit():  # Assuming this checks the validity of the data
                x, y, mnc, cid = parts[0], parts[1], parts[5], parts[6]
                measurement_point = (float(x), float(y))  # Convert to float tuple
                coords.append(measurement_point)  # Add to the set of unique coordinates
                
                # Open the locations file for LTE stations
                
                with open(f"daten/locations_{mode}.csv") as g:
                    for location_line in g.readlines():
                        l_parts = location_line.strip().split(',')
                        l_mnc, l_cid = l_parts[0].strip(), l_parts[1].strip()
                        # Check if there's a match
                        if mnc == l_mnc and cid == l_cid:
                            l_x, l_y = l_parts[3].strip(), l_parts[2].strip()
                            # Only add a line if the station has valid coordinates
                            if l_x != '?' and l_y != '?':
                                station_point = (float(l_x), float(l_y))  # Convert to float tuple
                                #coords.add(station_point)  # Add to set of unique coordinates
                                towers.add(station_point)
                                lines.append([measurement_point, station_point])

    # Check if we have any lines to plot, otherwise set a default location
    if lines:
        initial_location = lines[0][0]
    else:
        initial_location = [0, 0]  # Default location if no lines

    # Create a map centered around the first line's start coordinate
    m = folium.Map(location=initial_location, zoom_start=10)
    fg = folium.FeatureGroup(name="LTE Connections")

    # Add lines to the map
    for line in lines:
        folium.PolyLine(locations=line, weight=2, color='blue').add_to(fg)

    # Add markers for each unique coordinate
    for coord in towers:
        folium.Marker(location=coord, icon=folium.Icon(color='blue')).add_to(m)

    last_coord = coords[-1]
    for coord in coords:
        if coord not in towers:
            folium.PolyLine(locations=(last_coord, coord), weight=5, color='orange').add_to(fg)
            last_coord = coord
        

    fg.add_to(m)
    folium.LayerControl().add_to(m)

    # Save the map to an HTML file
    m.save(f'aufgabe3/lines_{file_name}.html')
