# -*- coding: utf-8 -*-
import csv
import os
import networkx as nx
import time
import zipfile
import shutil


# Function that read a csv file and return a list with a dict for each row
def csvToDictList(filename):
    with open(filename, 'r') as csvfile:
        csvdata = csv.DictReader(csvfile, delimiter=';')
        data = []

        for row in csvdata:
            data.append(row)

        # Transform strings into numbers (floatables only)
        for row in data:
            for key in row.keys():
                try:
                    row[key] = float(row[key].replace(',', '.'))
                except ValueError:
                    continue
    return data, csvdata.fieldnames


def is_number(x):  # Check if an element is a number
    try:
        float(x)
        return True
    except ValueError:
        return False


def saveGraph(graph, name='noname'):
    filename = "Results/"
    if graph.is_multigraph():
        filename += name + "-multigraph"
    else:
        filename += name + "-graph"

    filename += time.strftime("_%Y-%m-%d_%Hh%Mm%Ss")
    nx.write_gml(graph, filename)
    print('Graph saved as: ' + filename)


def saveGraphList(graphList, names, location='', timestamp=True):
    # Removing end slash if needed
    if location[-1] == '/':
        path = location[:-1]
    else:
        path = location

    # Adding timestamp
    if timestamp:
        ts = time.strftime("-%Y-%m-%d_%Hh%M")
        path += ts

    dirname = path + '/'
    os.makedirs(dirname, exist_ok=True)

    # Creating files
    if len(names) == len(graphList):
        for index in range(len(names) - 1):
            filename = dirname + names[index] + '.gml'
            nx.write_gml(graphList[index], filename)
        return {'dirname': dirname, 'path': path}
    else:
        print("Error when saving graphs : graphList's size and names's size don't match")
        return {}


def compressFolder(folder_path, clean=True, algo=zipfile.ZIP_LZMA):
    # Compressing files
    zf = zipfile.ZipFile(folder_path + '.zip', mode='w', compression=algo)
    folder_path += '/'
    for dirname, subdirs, files in os.walk(folder_path):
        # zf.write(dirname) # Uncomment to create the folder in the zip
        for filename in files:
            zf.write(os.path.join(dirname, filename), filename)
    zf.close()
    print('Folder \'' + folder_path + '\' compressed')

    # Cleaning files
    if clean:
        shutil.rmtree(dirname)
        print('Original files cleaned')
    else:
        print('Original files kept')


def showTime(start):
    print("--- %s seconds ---" % (time.time() - start))


def normalizeWeights(graph):
    maxW = 0
    minW = math.inf
    for edge in graph.edges():
        [u, v] = edge
        if graph[u][v]['weight'] > maxW:
            maxW = graph[u][v]['weight']
        if graph[u][v]['weight'] < minW:
            minW = graph[u][v]['weight']

    for edge in graph.edges():
        [u, v] = edge
        a = maxW - minW
        graph[u][v]['weight'] = (graph[u][v]['weight'] - minW) / a + 1
