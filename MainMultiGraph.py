# -*- coding: utf-8 -*-
import numpy as np
import networkx as nx
from SpectralData import *
from GraphGen import *
from GraphTools import *
from MultiGraph import MultiGraph
import time
import math

# Used to time the program
start = time.time()

##### Sample code to import CSV into a multigraph
file = "Data\FirstSet_09-2012_V2.csv"
persons, fieldnames = csvToDictList(file)
MG = MultiGraph()
MG.nodes = persons
# Generating graphs
MG.graphs, MG.fieldnames = genMultipleGraphs(persons, fieldnames, id_label='OrdreCIC')
MG.id_label = 'OrdreCIC'
for g in MG.graphs:
    # nx.k_core(g, 2)# Extracting subgraph with minimum node degree
    g = g.to_undirected()  # Converting graph to undirected
# Creating edges
i = 0
for graph in MG.graphs:
    node_list = graph.nodes()
    if is_number(graph.node[node_list[0]][MG.fieldnames[i]]):
        connectNodesQuantitative(graph, 3, attribute=MG.fieldnames[i])
    else:
        connectNodesQualitative(graph, attribute=MG.fieldnames[i])
    i += 1
print('Multigraph created')

##### Sample code to save MG to disk
# MG.save(location='Results/MultiGraph', ts=True, clean_files=True)
MG.save(location='MultiGraph', ts=False, clean_files=True)
showTime(start)

##### Sample code to load MG from disk
MG = MultiGraph()
MG.load('MultiGraph.zip')
showTime(start)

# Ignoring nodes not connected
for g in MG.graphs:
    g = nx.k_core(g, k=1)

##### Sample code to perform spectral clustering
SpectralDataList = []
for g in MG.graphs:
    for cc in nx.connected_component_subgraphs(g):
        # if cc.size() > 10:
        sd = SpectralData()
        sd.clusterNum = 5
        sd.graph = g
        SpectralDataList.append(sd)

# Processing
resultGraphList = []
for elem in SpectralDataList:
    if elem.buildProjections():
        elem.clusterize()
    resultGraphList.append(elem.graph)

# Count how many time nodes are in the same cluster
Adjacency = compareClusters(resultGraphList)

# Creating graph corresponding to adj
resGraph = adjToGraph(Adjacency, MG.nodes, MG.id_label)

# Normalizing weigths for edges
normalizeWeights(resGraph)

# Saving graph
nx.write_gml(resGraph, 'Results/resGraph.gml')
