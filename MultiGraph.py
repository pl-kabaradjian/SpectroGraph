import networkx as nx
from GraphTools import *
import zipfile
import csv
from io import StringIO, BytesIO


class MultiGraph:
    def __init__(self):
        self.nodes = []
        self.graphs = []
        self.fieldnames = []
        self.label_column = 'label'

    def load(self, filename="MultiGraph.zip"):

        fh = open(filename, 'rb')
        archive = zipfile.ZipFile(fh)
        filenamelist = archive.namelist()
        nb_gml = 0
        has_fn_file = False
        has_node_file = False
        for filename in filenamelist:
            if filename == 'fieldnames.csv':
                has_fn_file = True
                # data = archive.open(filename, 'r')
                data = BytesIO(archive.read(filename))
                data = data.read().decode('utf-8').split('\n')
                rdr = csv.reader(data, delimiter=';')
                self.fieldnames = next(rdr)
        self.label_column = self.fieldnames[0]

        for filename in filenamelist:
            if filename == 'nodes.csv':
                has_node_file = True
                # data = archive.open(filename, 'r')
                # data = StringIO(archive.read(filename))
                data = BytesIO(archive.read(filename))
                data = data.read().decode('utf-8').split('\n')
                node_reader = csv.DictReader(data, delimiter=';', fieldnames=self.fieldnames)
                for node in node_reader:
                    self.nodes.append(node)

        for filename in filenamelist:
            if filename.endswith('.gml'):
                nb_gml += 1
                data = archive.open(filename)
                dg = nx.DiGraph()
                dg = nx.read_gml(data)
                g = dg.to_undirected()
                self.graphs.append(g)

        if has_fn_file and has_node_file:
            print('Multigraph succesfully loaded with ' + str(nb_gml) + ' graphs')
        elif not has_fn_file:
            print('Missing fieldnames.csv')
        elif not has_node_file:
            print('Missing nodes.csv')

        if not (nb_gml > 0):
            print('Warning : no gml file has been loaded')

    def save(self, location='Results/MultiGraph', ts=True, clean_files=True):
        # Creating gmls
        paths = saveGraphList(self.graphs, self.fieldnames, location, ts)
        print('*.gml created')

        fn = [self.label_column]
        for x in self.fieldnames:
            fn.append(x)

        # Creating fieldnames.csv
        fn_file = open(paths['dirname'] + 'fieldnames.csv', 'w')
        wr = csv.writer(fn_file, delimiter=';')
        wr.writerow(fn)
        fn_file.close()
        print('fieldnames.csv created')

        # Creating nodes.csv
        nodes_file = open(paths['dirname'] + 'nodes.csv', 'w')
        # Recreating original csv fieldnames

        dwr = csv.DictWriter(nodes_file, fieldnames=fn, delimiter=';')

        for node in self.nodes:
            dwr.writerow(node)
        nodes_file.close()
        print('nodes.csv created')

        compressFolder(paths['path'], clean=clean_files, algo=zipfile.ZIP_DEFLATED)
