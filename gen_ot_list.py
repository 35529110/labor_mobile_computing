ot_set = set()
with open("daten/signal-2024-02-07-ot.csv") as f:
    for line in f.readlines():
        line = line.split(',')
        if str(line[2].strip()).isdigit():
            mnc = line[5]
            cid = line[6]
            ot_set.add((mnc,cid))
for entry in ot_set:
    print(entry)
