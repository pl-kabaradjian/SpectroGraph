# -*- coding: utf-8 -*-
import numpy as np
import networkx as nx
from SpectralData import SpectralData
from GraphGen import *
from GraphTools import *
from MultiGraph import MultiGraph
import time
import math

# Used to time the program
start_time = time.time()
print("--- %s seconds ---" % (time.time() - start_time))


# Importation des données à partir du fichier csv
file = "Data\FirstSet_09-2012_V2.csv"
persons, fieldnames = csvToDictList(file)
print("Importation OK")
print("--- %s seconds ---" % (time.time() - start_time))

# Generating graphs
multiple_graphs, names = genMultipleGraphs(persons, fieldnames, label='OrdreCIC')
for g in multiple_graphs:
    # nx.k_core(g, 2)# Recuperation du sous-graph avec des noeuds de degré 2 au moins
    g = g.to_undirected()  # Conversion en graph non-dirigé
print("Generation OK")
print("--- %s seconds ---" % (time.time() - start_time))


# Creating edges
i = 0
for graph in multiple_graphs:
    node_list = graph.nodes()
    if is_number(graph.node[node_list[0]][names[i]]):
        connectNodesQuantitative(graph, 3, attribute=names[i])
    else:
        connectNodesQualitative(graph, attribute=names[i])
    i += 1
print("Edges creation OK")
print("--- %s seconds ---" % (time.time() - start_time))

# Creating Multigraph object
MG = MultiGraph()
MG.nodes = persons
MG.graphs = multiple_graphs
MG.fieldnames = names
MG.label_column = 'OrdreCIC'

# Saving MG to disk
#MG.save(location='Results/MultiGraph', ts=True, clean_files=True)
MG.save(location='MultiGraph', ts=False, clean_files=True)
print("--- %s seconds ---" % (time.time() - start_time))

MG = MultiGraph()
MG.load('MultiGraph.zip')
print("--- %s seconds ---" % (time.time() - start_time))

# Ignoring nodes not connected
for g in MG.graphs:
    g = nx.k_core(g, k=1)
print("--- %s seconds ---" % (time.time() - start_time))

# Initializing spectral analysis
SpectralDataList = []

for g in MG.graphs:
    for cc in nx.connected_component_subgraphs(g):
        #if cc.size() > 10:
        sd = SpectralData()
        sd.clusterNum = 5
        sd.graph = g
        SpectralDataList.append(sd)

print("--- %s seconds ---" % (time.time() - start_time))

# Processing
resultGraphList = []
for elem in SpectralDataList:
    if elem.buildProjections():
        elem.clusterize()
    resultGraphList.append(elem.graph)

print("--- %s seconds ---" % (time.time() - start_time))

# Count how many time nodes are in the same cluster
Adj = {}

for subgraph in resultGraphList:

    adjdict = dict()
    # Iterating through nodes
    for startnode in subgraph.node.keys():
        # Checking if node exists in Adj
        if startnode in Adj:
            adjdict = Adj[startnode]

        if 'ClusterName' in subgraph.node[startnode]:
            current_cluster = subgraph.node[startnode]['ClusterName']

            for endnode in subgraph.node.keys():
                if startnode != endnode:
                    if 'ClusterName' in subgraph.node[endnode]:
                        if subgraph.node[endnode]['ClusterName'] == current_cluster:
                            if endnode in adjdict:
                                adjdict[endnode] += 1
                            else:
                                adjdict[endnode] = 1
        Adj[startnode] = adjdict

print("--- %s seconds ---" % (time.time() - start_time))
print(Adj.keys())

## Creating graph corresponding to adj
resGraph = nx.Graph()

# Adding nodes
for elem in MG.nodes:
    current_id_node = elem[MG.label_column]  # getting node id
    resGraph.add_node(current_id_node, elem)
    # for key in elem.keys():
    #     resGraph.node[current_id_node][key] = elem[key]

# Creating edges from Adj
for xnode in Adj.keys():
    for ynode in Adj[xnode].keys():
        if not resGraph.has_edge(str(xnode), str(ynode)) and not ynode == xnode:
            resGraph.add_edge(str(xnode), str(ynode), {'weight': Adj[xnode][ynode]})

# Normalizing weigths for edges
maxW = 0
minW = math.inf
for edge in resGraph.edges():
    [u, v] = edge
    if resGraph[u][v]['weight'] > maxW:
        maxW = resGraph[u][v]['weight']
    if resGraph[u][v]['weight'] < minW:
        minW = resGraph[u][v]['weight']

for edge in resGraph.edges():
    [u, v] = edge
    a = maxW - minW
    resGraph[u][v]['weight'] = (resGraph[u][v]['weight'] - minW) / a + 1

# Saving graph
nx.write_gml(resGraph, 'Results/resGraph.gml')
