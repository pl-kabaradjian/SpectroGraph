import networkx as nx
from GraphTools import *
import csv

class MultiGraph:
    def __init__(self):
        self.nodes = [{}]
        self.graphs = [nx.Graph()]
        self.fieldnames = []

    def load(self, filename="MultiGraph.zip"):



        print('')

    def save(self):
        # Creating gmls
        paths = saveGraphList(self.graphs, self.fieldnames)
        print('*.gml created')

        # Creating fieldnames.csv
        fn_file = open(paths['dirname'] + 'fieldnames.csv', 'w')
        wr = csv.writer(fn_file, delimiter=';')
        wr.writerow(self.fieldnames)
        fn_file.close()
        print('fieldnames.csv created')

        # Creating nodes.csv
        nodes_file = open(paths['dirname'] + 'nodes.csv', 'w')
        dwr = csv.DictWriter(nodes_file, fieldnames=self.fieldnames, delimiter=';')
        for node in self.nodes:
            dwr.writerow(node)
        nodes_file.close()
        print('nodes.csv created')

        compressFolder(paths['path'], clean=True)