#author:Hamza Reza Pavel
#Datastructure to represent HoMLN using networkx undirectional graph.

import networkx as nx
import os

class MLN:

    def __init__(self):
        self.layers = []
        self.directory = os.getcwd()

    def get_all_layer(self):
        return self.layers

    def get_nth_layer(self, n):
        return self.layers[n]

    def add_layer(self, g):
        self.layers.append(g)

    def get_number_of_layers(self):
        return len(self.layers)

    def __aggregate_graph_AND(self, g1, g2):
        nodes = g1.nodes
        resultGraph = nx.Graph()
        resultGraph.add_nodes_from(nodes)
        edges_g1 = set([e for e in g1.edges])
        edges_g2 = set([e for e in g2.edges])
        common_edges = edges_g1.intersection(edges_g2)
        resultGraph.add_edges_from(common_edges)
        return resultGraph;

    def __aggregate_graph_OR(self, g1, g2):
        nodes = g1.nodes
        resultGraph = nx.Graph()
        resultGraph.add_nodes_from(nodes)
        edges_g1 = set([e for e in g1.edges])
        edges_g2 = set([e for e in g2.edges])
        output_edges = edges_g1.union(edges_g2)
        resultGraph.add_edges_from(output_edges)
        return resultGraph

    def get_aggregated_graph_AND(self):
        resultGraph = self.layers[0]
        for i in range(1, len(self.layers)):
            resultGraph = self.__aggregate_graph_AND(resultGraph, self.layers[i])
        return resultGraph;

    def get_aggregated_graph_OR(self):
        resultGraph = self.layers[0]
        for i in range(1, len(self.layers)):
            resultGraph = self.__aggregate_graph_OR(resultGraph, self.layers[i])

        return resultGraph;
