import networkx as nx
import numpy as np
import networkx as nx
from sklearn.cluster import SpectralClustering

#importation du graph à partir du fichier gml
GraphD = nx.read_gml('graphdumps1479935148.gml', label='label')
#GraphD = nx.read_gml('double_anneau.gml', label='label')
print("Importation OK")
nx.k_core(GraphD, 2)#Recuperation du sous-graph avec des noeuds de degré 2 au moins
Graph = GraphD.to_undirected()#Conversion en graph non-dirigé

clusterNum = 30

adj = nx.adjacency_matrix(Graph, weight='count')
print("Adj OK")
SC_est = SpectralClustering(n_clusters=clusterNum, affinity='precomputed',n_init=100, n_jobs=-2)
labels = SC_est.fit_predict(adj)

#Creation des clusters
nodes = Graph.nodes()
clusters = {}
for i in range(0, clusterNum):
    k = []  # liste des noeuds du meme cluster
    for j in range(len(labels)):
        if labels[j] == i:
            k.append(j)
    if len(k) > 0:
        members = [nodes[index] for index in k]
        #center_node = self.set_cluster_center(labels, method='centrality')
        #self.clusters[center_node[0]] = {'members': labels, 'size': len(labels), 'center': center_node}
        for member in members:
            Graph.node[member]['ClusterName'] = i
    else:
        print('Empty cluster')

#Sauvegarde des résultats
nx.write_gml(Graph, 'result_sklean_SC.gml')
#nx.write_gml(Graph, 'result_double_anneau_sklean_SC.gml')
print('Graph saved')