import networkx as nx
from MLN import MLN
import os

def read_mln(directory_path):
    mln = MLN()
    path = directory_path
    for filename in os.listdir(path):
        if not filename.startswith('.'):
            with open(os.path.join(path, filename), 'r') as infile:
                layer = nx.Graph()
                for i, line in enumerate(infile):
                    line = line.strip('\n')
                    edgeInfo = line.split(",")
                    v1=int(edgeInfo[0])
                    v2=int(edgeInfo[1])
                    layer.add_node(v1)
                    layer.add_node(v2)
                    layer.add_edge(v1,v2)
                mln.add_layer(layer)

            infile.close()
    return mln


#used to read layers from RMAT generated format. requires the nodecount in the graph.
'''def read_PaRMAT_graphs(directory_path, nodecount):
    mln = mlnlib.MLN()
    path = directory_path
    for filename in os.listdir(path):
        if not filename.startswith('.'):
            with open(os.path.join(path, filename), 'r') as infile:
                layername = ""
                layer = nx.Graph()
                for i in range(nodecount):
                    layer.add_node(i)
                for i, line in enumerate(infile):
                    line = line.strip('\n')
                    edge = line.split("\t")
                    layer.add_edge(int(edge[0]), int(edge[1]))
                mln.add_layer(layer)
            infile.close()
    return mln'''


#writes the MLN to files. each file is created for the layers in the network.
def write_mln_to_file(mln, path):
    for i in range(0, mln.get_number_of_layers()):
        filename = "layer_" + (str(i))
        g = mln.get_nth_layer(i)
        path_to_file = os.path.join(path, filename)
        os.makedirs(os.path.dirname(path_to_file), exist_ok=True)
        with open(path_to_file, 'w') as file:
            file.write(filename)
            file.write("\n")
            file.write(str(g.number_of_nodes()))
            file.write("\n")
            file.write(str(g.number_of_edges()))
            file.write("\n")
            for i in g.nodes():
                file.write(str(i))
                file.write("\n")
            for e in g.edges:
                file.write(f"{e[0]},{e[1]},1.0")
                file.write("\n")
        file.close()
