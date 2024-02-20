from matplotlib import pyplot as plt
from matplotlib import cm
import os
import random


files = list(filter(lambda s: s.endswith(".csv"), os.listdir('daten/')))
file_ot = list(filter(lambda s: s.endswith("-ot.csv"), files))[0]
file_mt = list(filter(lambda s: s.endswith("-mt.csv"), files))[0]

index_data = ['gps-l', 'gps-b', 'height', 'MCC', 'MNC', 'LAC', 'CID', 'strength', 'LTE1', 'LTE2', '', '']
index_262 = ['LTE', 'MCC', 'MNC', 'LAC', 'CID', '', 'gps-l', 'gps-b', '', '', '', '', '', '']


def get_cell_id_set(data:list) -> set:
    return set([p['CID'] for p in data])

def load_data(file_name:str) -> list:
    file = open("daten/"+file_name, "r")
    data = [l[:-1].split(',') for l in file.readlines()]
    file.close()
    return data

def clean_data(data:list) -> list:
    cleaned_data = []
    keys = [('gps-l', float), ('gps-b', float), ('CID', int), ('strength', int)]
    for point in data:
        cleaned_data.append({})
        for key, dtype in keys:
            cleaned_data[-1][key] = dtype(point[index_data.index(key)])
    return cleaned_data

def get_cell_towers(data:list) -> list:
    keys = [('MCC', int), ('MNC', int), ('LAC', int), ('CID', int)]
    cleaned_data = set()
    for point in data:
        new_tower = []
        for key, dtype in keys:
            new_tower.append(dtype(point[index_data.index(key)]))
        cleaned_data.add(tuple(new_tower))
    return list(cleaned_data)


def plot_data(data, name):
    cell_id_list = list(get_cell_id_set(data))
    strength_list = [d['strength'] for d in data]
    color_map = [cm.jet(cell_id_list.index(d['CID'])/len(cell_id_list)) for d in data]
    plt.title(name)
    plt.ylim([-125, 0])
    plt.bar(range(len(data)), strength_list, width=1, color=color_map)
    plt.savefig(name+'.png')
    plt.close()


def clean_262() -> None:
    file = open('daten/262.csv', 'r')
    data = []
    n = 0
    line = file.readline()
    print(line.split(','))
    while True:
        n += 1
        line = file.readline()
        if line == "":
            break
        if n%1000 == 0:
            print(f"{round(n/29139, 2)}%")
        line = line[:-1].split(',')
        #if line[0] != "LTE":
        #    continue
        #if line[2] != '1':
        #    continue
        if line[3] != "3080" and line[3] != "4012":
            continue
        data.append(line)
    file.close()
    print('all data loaded')

    file = open('daten/262_cleaned.csv', 'w')
    for line in data:
        for point in line[:-1]:
            file.write(point+",")
        file.write(line[-1])
        file.write("\n")
    file.close()
    print("all data saved")

def load_clened_262() -> list:
    file = open("daten/262_cleaned.csv", "r")
    lines = file.readlines()
    file.close()
    data = [l[:-1].split(',') for l in lines]
    return data

raw_data_mt = load_data(file_mt)
raw_data_ot = load_data(file_ot)

cell_towers_mt = get_cell_towers(raw_data_mt)
cell_towers_ot = get_cell_towers(raw_data_ot)

data_mt = clean_data(raw_data_mt)
data_ot = clean_data(raw_data_ot)

clean_262()

towers = load_clened_262()

cids = list(map(lambda t: t[3], cell_towers_mt))
new_towers = []
for tower in towers:
    if int(tower[index_262.index('CID')]) in cids:
        new_towers.append(tower)
print(new_towers, len(new_towers))


#plot_data(data_mt, 'signal_plot_mt')
#plot_data(data_ot, 'signal_plot_ot')

#print('mt', len(data_mt), len(get_cell_id_set(data_mt)))
#print('ot', len(data_ot), len(get_cell_id_set(data_ot)))

#print("od/mt", list(filter(lambda d: d not in get_cell_id_set(data_mt), get_cell_id_set(data_ot))))
#print("mt/ot", list(filter(lambda d: d not in get_cell_id_set(data_ot), get_cell_id_set(data_mt))))

#print(cell_towers_mt)
#print(cell_towers_ot)

