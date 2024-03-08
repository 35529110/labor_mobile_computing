import colorsys
import folium
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def get_heatmap_color(value):
    norm = mcolors.Normalize(vmin=0, vmax=1)
    cmap = plt.cm.plasma  # Du kannst hier auch andere Colormaps auswählen (z.B. 'viridis', 'plasma', 'inferno', usw.)

    rgba_color = cmap(norm(value))
    rgb_color = (rgba_color[0], rgba_color[1], rgba_color[2])

    return rgb_color

files = filter(lambda s: s.startswith('signal'), os.listdir("daten"))

lines = []  # Store lines between measurement points and LTE stations
coords = []  # Use a set to avoid duplicate points



for file_name in files:
    max_sig = -1000
    min_sig = 0
    # Open the measurement data file
    with open("daten/signal-2024-02-07-ot.csv") as f:
        for line in f.readlines():
            parts = line.strip().split(',')
            # Check if the coordinate parts are valid numbers
            if not parts[2].isdigit():  # Assuming this checks the validity of the data
                continue
            x, y, mnc, cid, sig = parts[0], parts[1], parts[5], parts[6], parts[7]
            measurement_point = (float(x), float(y), int(sig))  # Convert to float tuple
            coords.append(measurement_point)  # Add to the set of unique coordinates
            min_sig = min(min_sig, int(sig))
            max_sig = max(max_sig, int(sig))
            

    print(max_sig, min_sig)
    for i in range(len(coords)-1):
        color_index = (coords[i][2]-max_sig) / (min_sig-max_sig)
        lines.append((coords[i][:2], coords[i+1][:2], color_index))


    # Create a map centered around the first line's start coordinate
    m = folium.Map(location=lines[0][0], zoom_start=10)
    fg = folium.FeatureGroup(name="LTE Connections")

    # Add lines to the map
    for line in lines:
        #rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(line[2], 1, 1))
        rgb = get_heatmap_color(line[2])
        rgb = [int(c*255) for c in rgb]
        color = '#%02x%02x%02x' % tuple(rgb)
        folium.PolyLine(locations=line[:2], weight=10, color=color).add_to(fg)

        

    fg.add_to(m)
    folium.LayerControl().add_to(m)

    # Save the map to an HTML file
    m.save(f'aufgabe3/path_{file_name}.html')
