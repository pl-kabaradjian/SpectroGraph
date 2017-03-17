# -*- coding: utf-8 -*-
import networkx as nx
from operator import itemgetter
from GraphTools import *


# function that generate a graph from a list of dict
# each row will become a node
def genGraph(dictList, fieldnames, multigraph=False):
    if multigraph:
        graph = nx.MultiGraph()
    else:
        graph = nx.Graph()

    # Adding nodes with attributes
    for elem in dictList:
        current_id_node = elem[fieldnames[0]]  # getting first filename as node id
        graph.add_node(current_id_node)
        for key in elem.keys():
            graph.node[current_id_node][key] = elem[key]
    return graph


# function that generates one graph for each column
# returns a list of nx.Graph
def genMultipleGraphs(dictList, fieldnames, label='label'):
    glist = []
    names = []

    for column in fieldnames:
        if column != label:
            curr_graph = nx.Graph()
            for elem in dictList:
                current_id_node = elem[label]  # getting id field
                curr_graph.add_node(current_id_node, attr_dict={column: elem[column]})
                #curr_graph.node[current_id_node][column] = elem[column]  # one attribute by node
            glist.append(curr_graph)
            names.append(column)

    return glist, names


def connectNodesQualitative(graph, attribute='label'):
    # Adding edges between equal node attributes
    node_list = graph.nodes()

    for src_node_id in node_list:
        for dst_node_id in node_list:
            if src_node_id != dst_node_id:
                src_node = graph.node[src_node_id]
                dst_node = graph.node[dst_node_id]
                if not is_number(src_node[attribute]) and not is_number(dst_node[attribute]):#check for no-number value
                    if dst_node[attribute] == src_node[attribute]:
                        if not graph.has_edge(src_node_id, dst_node_id):
                            graph.add_edge(src_node_id, dst_node_id, attr_dict={'weight': 1})


def connectNodesQuantitative(graph, nearest_neighbours=3, attribute='label'):
    # knn graph
    node_list = graph.nodes()
    #node_list.sort()

    for src_node_id in node_list:
        src_node = graph.node[src_node_id]
        if is_number(src_node[attribute]):
            dist_list = []

            # Computing attribute distance
            for dst_node_id in node_list:
                dst_node = graph.node[dst_node_id]
                if src_node_id != dst_node_id and is_number(dst_node[attribute]):
                    temp = []
                    dist = dst_node[attribute] - src_node[attribute]
                    # print([src_node_id,':',src_node[key],dst_node_id,':',dst_node[key],key])
                    dist = pow(dist, 2)
                    temp = [dst_node_id, dist]
                    dist_list.append(temp)

            # Sorting distance list
            dist_list.sort(key=itemgetter(1))

            # Connecting k nearest neighbors
            for i in range(nearest_neighbours - 1):
                src = src_node_id
                dst = dist_list[i][0]
                if not graph.has_edge(src, dst):
                    # graph.add_edge(src, dst, type=str(key))
                    if dist_list[i][1] == 0:
                    if dist_list[i][1] == 0:
                        weight = 1
                    else:
                        weight = 1/dist_list[i][1]
                    graph.add_edge(src, dst, weight=weight)
