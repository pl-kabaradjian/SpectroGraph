# -*- coding: utf-8 -*-
import csv
import networkx as nx

file = "Data\FirstSet_09-2012_V2.csv"

#Function that read the csv file and return a list with a dict for each row
def readCsv(filename):
    with open(filename, 'r') as csvfile:
        csvdata = csv.DictReader(csvfile, delimiter=';')
        data = []

        for row in csvdata:
            data.append(row)
    return data, csvdata.fieldnames

persons, fieldnames = readCsv(file)

#function that generate a graph from a list of dict
#each row will become a node
def genGraph(dictList, fieldnames):
    graph = nx.Graph()
    #Adding nodes with attributes
    for elem in dictList:
        current_id_node = elem[fieldnames[0]]# getting first filename as node id
        graph.add_node(current_id_node)
        for key in elem.keys():
            graph.node[current_id_node][key] = elem[key]

    #Adding edges between attributes
    node_list = graph.nodes()
    for src_node_id in node_list:
        for dst_node_id in node_list:
            if src_node_id != dst_node_id:
                src_node = graph.node[src_node_id]
                dst_node = graph.node[dst_node_id]
                for key in src_node.keys():
                    i = fieldnames.index(key)
                    if dst_node[key] == src_node[key]:
                        if not graph.has_edge(src_node_id,dst_node_id):
                            edge = graph.add_edge(src_node_id,dst_node_id)
                            #graph.edge[src_node_id][dst_node_id][key] = src_node[key]
                            graph.edge[src_node_id][dst_node_id]['size'] = 1
                        else:
                            graph.edge[src_node_id][dst_node_id]['size'] += 1
    return graph

g = genGraph(persons, fieldnames)

nx.write_gml(g, 'Results\medical_graph.gml')
print('Graph saved')

print('OK')