# -*- coding: utf-8 -*-
import numpy as np
import networkx as nx
from sklearn.cluster import KMeans
# import scipy as sc
from scipy.sparse import csr_matrix, spdiags
from scipy.sparse.linalg import eigsh


class SpectralData:
    def __init__(self):
        self.graph = nx.Graph()
        self.size = 0
        self.normv = []
        self.clusterNum = 0
        self.clusters = {}
        self.mu = []

    def buildProjections(self):
        print('Building projections')

        # adj
        adj = nx.adjacency_matrix(self.graph, weight='weight')
        # deg
        deg = adj.sum(axis=0)
        # choix du nombre de dimensions
        k_dim = min(int(0.9 * adj.shape[0]), 30)
        # calcul du laplacien
        lap = nx.laplacian_matrix(self.graph, weight='weight').asfptype()
        lap *= -1
        # Rescaling ?
        diag = np.array(deg[0]).astype(float)
        m = spdiags(diag, 0, diag.shape[1], diag.shape[1])
        # calcul des valeurs propres
        try:
            lambdas, maps = eigsh(A=lap, M=m, k=k_dim, sigma=1.0, which='LM')
            self.normv = maps  # /np.amax(maps)
            print('Projections built')
            return True
        except:
            print('Cannot build projections')
            return False

    def cluster_nodes(self):

        estimator = KMeans(n_clusters=self.clusterNum, init='k-means++', precompute_distances=True, n_init=20,
                           max_iter=1000)
        # estimator = KMeans(n_clusters=2, init='k-means++', precompute_distances=True, n_init=20,max_iter=1000)

        estimated_labels = estimator.fit_predict(self.normv)
        nodes = self.graph.nodes()
        self.clusters = {}
        for i in range(0, self.clusterNum):
            k = []  # liste des noeuds du meme cluster
            for j in range(len(estimated_labels)):
                if estimated_labels[j] == i:
                    k.append(j)

            if len(k) > 0:
                labels = [nodes[index] for index in k]
                center_node = self.set_cluster_center(labels, method='centrality')
                self.clusters[center_node[0]] = {'members': labels, 'size': len(labels), 'center': center_node}
                for label in labels:
                    self.graph.node[label]['ClusterName'] = center_node[0]
            else:
                print('Empty cluster')

    def set_cluster_center(self, members, method):
        subgraph = self.graph.subgraph(members)
        if len(subgraph) > 1:
            max_value = 0
            max_node_id = ''
            if method == 'centrality':
                # Searching for node with maximal centrality
                s = 1.0 / (len(subgraph) - 1.0)
                centrality = dict((n, d * s) for n, d in subgraph.degree_iter())
                for key in centrality:
                    if centrality[key] > max_value:
                        max_value = centrality[key]
                        max_node_id = key
                center_node = [max_node_id, max_value]
            elif method == 'degree':
                # Searching for node with max degree
                for key in members:
                    if self.graph.degree(key) > max_value:
                        max_value = self.graph.degree(key)
                        max_node_id = key
                center_node = [max_node_id, max_value]
        else:
            center_node = [subgraph.nodes()[0], 0]
        return center_node

    def clusterize(self):
        # print('Clustering')
        self.cluster_nodes()
        print('Clustering OK')

    def saveGraph(self, name='result.gml'):
        nx.write_gml(self.graph, name)
        print('Graph saved')

    def fullProcess(self):
        print('Starting full process')

        self.buildProjections()
        self.clusterize()

        print('End of process')


def compareClusters(clusteredGraphs):
    Adj = {}
    for subgraph in clusteredGraphs:

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
    return Adj


def adjToGraph(adj, nodeList, idLabel):
    resGraph = nx.Graph()

    # Adding nodes
    for elem in nodeList:
        current_id_node = elem[idLabel]  # getting node id
        resGraph.add_node(current_id_node, elem)
        # for key in elem.keys():
        #     resGraph.node[current_id_node][key] = elem[key]

    # Creating edges from Adj
    for xnode in adj.keys():
        for ynode in adj[xnode].keys():
            if not resGraph.has_edge(str(xnode), str(ynode)) and not ynode == xnode:
                resGraph.add_edge(str(xnode), str(ynode), {'weight': adj[xnode][ynode]})

    return resGraph
