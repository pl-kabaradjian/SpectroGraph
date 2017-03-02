# -*- coding: utf-8 -*-
import csv
import os
import networkx as nx
import time
import zipfile
import zlib
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


def saveGraphList(graphList, names):
    ts = time.strftime("%Y-%m-%d_%Hh%M")
    dirname = "Results/MultiGraph-" + ts
    zipname = dirname + '.zip'
    dirname += '/'
    os.makedirs(dirname, exist_ok=True)

    # Creating files
    if len(names) == len(graphList):
        for index in range(len(names) - 1):
            filename = dirname + names[index] + '-graph.gml'
            nx.write_gml(graphList[index], filename)
    else:
        print("Error when saving graphs : graphList's size and names's size don't match")

    # Compressing files
    zf = zipfile.ZipFile(zipname, mode='w', compression=zipfile.ZIP_LZMA)
    for dirname, subdirs, files in os.walk(dirname):
        #zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename),filename)
    zf.close()

    # Cleaning files
    shutil.rmtree(dirname)