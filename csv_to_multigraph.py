# -*- coding: utf-8 -*-
import csv
import os
import networkx as nx
from operator import itemgetter
import time

file = "Data\FirstSet_09-2012_V2.csv"


# Function that read the csv file and return a list with a dict for each row
def readCsv(filename):
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


persons, fieldnames = readCsv(file)


# function that generate a graph from a list of dict
# each row will become a node
def genGraph(dictList, fieldnames):
    graph = nx.Graph()
    # Adding nodes with attributes
    for elem in dictList:
        current_id_node = elem[fieldnames[0]]  # getting first filename as node id
        graph.add_node(current_id_node)
        for key in elem.keys():
            graph.node[current_id_node][key] = elem[key]
    return graph


# function that generate a multigraph from a list of dict
# each row will become a node
def genMultigraph(dictList, fieldnames):
    graph = nx.MultiGraph()
    # Adding nodes with attributes
    for elem in dictList:
        current_id_node = elem[fieldnames[0]]  # getting first field as node id
        graph.add_node(current_id_node)
        for key in elem.keys():
            graph.node[current_id_node][key] = elem[key]
    return graph


# function that generates one graph for each column
# returns a list of nx.Graph
def genMultipleGraphs(dictList, fieldnames):
    glist = []

    for column in fieldnames:
        curr_graph = nx.Graph()
        for elem in dictList:
            current_id_node = elem[fieldnames[0]]  # getting first field as node id
            curr_graph.add_node(current_id_node)
            curr_graph.node[current_id_node][column] = elem[column]  # one attribute by node
        glist.append(curr_graph)

    return glist, fieldnames


def connectNodesQualitative(graph):
    # Adding edges between equal node attributes
    node_list = graph.nodes()

    for src_node_id in node_list:
        for dst_node_id in node_list:
            if src_node_id != dst_node_id:
                src_node = graph.node[src_node_id]
                dst_node = graph.node[dst_node_id]
                for key in src_node.keys():
                    if not is_number(src_node[key]):
                        if dst_node[key] == src_node[key]:
                            if not graph.has_edge(src_node_id, dst_node_id):
                                # graph.add_edge(src_node_id, dst_node_id, type=key)
                                graph.add_edge(src_node_id, dst_node_id, attr_dict={'Weight': 1, 'type': key})
                                # graph.edge[src_node_id][dst_node_id]['Weight'] = 1
                            else:
                                # w = graph.edge[src_node_id][dst_node_id][0]['Weight'] + 1
                                w = graph.edge[src_node_id][dst_node_id]['Weight'] + 1
                                graph.add_edge(src_node_id, dst_node_id, attr_dict={'Weight': w, 'type': key})


def connectNodesQuantitative(graph, nearest_neighbours=3):
    # knn graph
    node_list = graph.nodes()
    node_list.sort()

    for src_node_id in node_list:
        src_node = graph.node[src_node_id]
        for key in src_node.keys():
            if is_number(src_node[key]):
                dist_list = []
                # Computing attribute distance
                for dst_node_id in node_list:
                    dst_node = graph.node[dst_node_id]
                    if src_node_id != dst_node_id and is_number(dst_node[key]):
                        temp = []
                        dist = dst_node[key] - src_node[key]
                        # print([src_node_id,':',src_node[key],dst_node_id,':',dst_node[key],key])
                        dist = pow(dist, 2)
                        temp = [dst_node_id, dist]
                        dist_list.append(temp)
                dist_list.sort(key=itemgetter(1))
                for i in range(nearest_neighbours - 1):
                    src = src_node_id
                    dst = dist_list[i][0]
                    if not graph.has_edge(src, dst):
                        # graph.add_edge(src, dst, type=str(key))
                        graph.add_edge(src, dst)


def is_number(x):  # Check if an element is a number
    try:
        float(x)
        return True
    except ValueError:
        return False


def saveGraph(graph, name='random'):
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
    dirname = "Results/MultiplesGraphs-" + ts + '/'
    os.makedirs(dirname, exist_ok=True)

    if len(names) == len(graphList):
        for index in range(len(names) - 1):
            filename = dirname + names[index] + '-graph.gml'
            nx.write_gml(graphList[index], filename)
    else:
        print("Error when saving graphs : graphList's size and names's size don't match")


multiple_graphs, names = genMultipleGraphs(persons, fieldnames)

i = 0
for graph in multiple_graphs:
    node_list = graph.nodes()
    if is_number(graph.node[node_list[0]][names[i]]):
        connectNodesQuantitative(graph, 3)
    else:
        connectNodesQualitative(graph)
    i += 1
saveGraphList(multiple_graphs, names)

# g = genGraph(persons, fieldnames)
# g = genMultigraph(persons, fieldnames)
# connectNodesQualitative(g)
# connectNodesQuantitative(g, nearest_neighbours=3)
# saveGraph(g, 'cancer')

print('OK')
