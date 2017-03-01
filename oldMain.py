# -*- coding: utf-8 -*-
import numpy as np
import networkx as nx
from SpectralData import SpectralData

# importation du graph à partir du fichier gml
GraphD = nx.read_gml('Data\graphdumps1479935148.gml', label='id')
# GraphD = nx.read_gml('double_anneau.gml', label='label')
print("Importation OK")
nx.k_core(GraphD, 2)  # Recuperation du sous-graph avec des noeuds de degré 2 au moins
Graph = GraphD.to_undirected()  # Conversion en graph non-dirigé

# Initialisation
sd = SpectralData()
sd.clusterNum = 30
sd.graph = Graph

# Processing
# sd.fullProcess()
sd.buildProjections()
iterations = []
for i in range(5):
    sd.cluster_nodes()
    iterations.append(sd.clusters)

nodes = sd.graph.nodes()

hist = {}  # contient pour chaque noeud les différents clusters attribués

for node in nodes:
    hist[node] = []
    for clusters in iterations:
        for key in clusters.keys():
            current_cluster = clusters[key]
            if node in current_cluster['members']:
                hist[node].append(current_cluster['center'])

print(' ')

# saving results
# sd.saveGraph('Results\result_double_anneau.gml')*
# sd.saveGraph('Results\result.gml')
