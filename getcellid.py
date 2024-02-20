coords = list()
with open("daten/locations_ot.csv") as f:
    for line in f.readlines():
        messurement = line.split(',')
        area_m = messurement[0].strip()
        cellid_m = messurement[1].strip()
        with open("daten/262.csv") as g:
            found = 0
            lookup = ""
            for line in f.readlines():
                lookup = line.split(',')
                area = lookup[3]
                cellid = lookup[4]
                if area_m == area and cellid_m == cellid:
                    lon = lookup[6]
                    lat = lookup[7]
                    coords.append((lon, lat))
                    found = 1
                    break
            if not found:
                print(f"unkown tower, {lookup}")
for i in coords:
    print(i)
