# -*- coding: utf-8 -*-
import numpy as np
import networkx as nx
from SpectralData import SpectralData
from GraphGen import *
from GraphTools import *
from MultiGraph import MultiGraph

# Importation des données à partir du fichier csv
file = "Data\FirstSet_09-2012_V2.csv"
persons, fieldnames = csvToDictList(file)
print("Importation OK")

# Generating graphs
multiple_graphs, names = genMultipleGraphs(persons, fieldnames)
for g in multiple_graphs:
    # nx.k_core(g, 2)# Recuperation du sous-graph avec des noeuds de degré 2 au moins
    g = g.to_undirected()  # Conversion en graph non-dirigé
print("Generation OK")


# Creating edges
i = 0
for graph in multiple_graphs:
    node_list = graph.nodes()
    if is_number(graph.node[node_list[0]][names[i]]):
        connectNodesQuantitative(graph, 3)
    else:
        connectNodesQualitative(graph)
    i += 1
print("Edges creation OK")

# Creating Multigraph object
MG = MultiGraph()
MG.nodes = persons
MG.graphs = multiple_graphs
MG.fieldnames = names

# Saving MG to disk
MG.save()


# Initialisation de l'analyse spectrale
# SpectralDataList = []
#
# for g in multiple_graphs:
#     sd = SpectralData()
#     sd.clusterNum = 30
#     sd.graph = g
#     SpectralDataList.append(sd)
#
# saveGraphList(multiple_graphs, names)
#
# # Processing
# resultGraphList = []
# for elem in SpectralDataList:
#     if elem.buildProjections():
#         elem.clusterize()
#     resultGraphList.append(elem.graph)
#
# saveGraphList(resultGraphList, names)

# iterations = []
# for i in range(5):
#     sd.cluster_nodes()
#     iterations.append(sd.clusters)
#
# nodes = sd.graph.nodes()
# hist = {} # contient pour chaque noeud les différents clusters attribués
#
# for node in nodes:
#     hist[node] = []
#     for clusters in iterations:
#         for key in clusters.keys():
#             current_cluster = clusters[key]
#             if node in current_cluster['members']:
#                 hist[node].append(current_cluster['center'])

# # saving results
# saveGraphList(multiple_graphs, names)
# print('Graphs saved')
