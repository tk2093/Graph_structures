import networkx as nx
import MLN_IO as mlnio
import MLN as mlnlib
import statistics as stat
from collections import Counter
import csv
import matplotlib.pyplot as plt
import sys
import os


def plot_degree_histogram_v3(graph, layername, save_file_path):
    counts = Counter(d for n, d in graph.degree())
    degree_freq = [counts.get(i, 0) for i in range(max(counts) + 1)]
    #print(degree_freq)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([k for k in range(0, len(degree_freq))], [v for v in degree_freq])
    #ax.set_yscale('log')
    #ax.set_xscale('log')
    plt.title(f"{layername} Degree Distribution")
    plt.xlabel('Degree')
    plt.ylabel('Number of nodes')
    #plt.show() # blocking function. commented out to stop interrupting the exeuction of code in batch mode.
    fig.savefig(save_file_path+"_"+layername+"_deg_dist"+".png")

def degree_statistics(graph):
    degrees = [v for k, v in graph.degree()]
    #print(degrees)
    minimum = min(degrees)
    maximum = max(degrees)
    avg = stat.mean(degrees)
    stdev = stat.stdev(degrees)
    return minimum, maximum, avg, stdev, degrees

def network_sum():
    #datasetpath = sys.argv[1]
    #output_path = sys.argv[2]
    datasetpath = 'PathToInputDirectory'
    output_path = 'PathToOutputDirectory/output.txt'
    #mln = read_PaRMAT_graphs(datasetpath, number_of_nodes_per_layer)
    mln = mlnio.read_mln(datasetpath)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, mode='w') as analysis_file:
            fieldnames = ['number_of_nodes', 'number_of_edges', 'density',
                          'number_of_connected_comp', 'connected_comps','diameter',
                          'min_degree','max_degree', 'avg_degree','std_dev_degree']
            writer = csv.DictWriter(analysis_file, fieldnames=fieldnames)
            writer.writeheader()

    print("Begin Network Summary\n\n")

    for i in range(mln.get_number_of_layers()):
        g1 = mln.get_nth_layer(i)
        number_of_nodes = g1.number_of_nodes()
        print(f"number of nodes of layer {i} : {number_of_nodes}")
        num_of_edges = g1.number_of_edges()
        print(f"number of edges of layer {i}: {num_of_edges}")
        connected_component_g1 = [len(c) for c in sorted(nx.connected_components(g1), key=len, reverse=True)]
        print(f"Number of Connected Component of layer {i}   :{len(connected_component_g1)} ")
        density_g1 = nx.density(g1)
        print(f"Density of layer {i}  : {density_g1}")

        diameter = -1
        if len(connected_component_g1) == 1:
            diameter = nx.diameter(g1)
            print(f"diameter of layer {i}: {diameter}") #diameter is only defined in nx if the whole graph is a singel connected component.

        #print([number_of_nodes, num_of_edges, density_g1, len(connected_component_g1)])
        plot_degree_histogram_v3(g1, f"layer{i}", output_path)

        minimum_deg_g1, maximum_deg_g1, avg_deg_g1, stdev_deg_g1, degrees_g1 = degree_statistics(g1)

        with open(output_path, mode='a') as analysis_file:
            fieldnames = ['number_of_nodes', 'number_of_edges', 'density',
                          'number_of_connected_comp', 'connected_comps','diameter',
                          'min_degree','max_degree', 'avg_degree','std_dev_degree']
            writer = csv.DictWriter(analysis_file, fieldnames=fieldnames)
            writer.writerow({'number_of_nodes':number_of_nodes, 'number_of_edges':num_of_edges, 'density':density_g1,
                          'number_of_connected_comp':len(connected_component_g1), 'connected_comps':connected_component_g1,'diameter': diameter,
                          'min_degree':minimum_deg_g1,'max_degree':maximum_deg_g1, 'avg_degree':avg_deg_g1,'std_dev_degree': stdev_deg_g1})

        print("End network summary. Additional files are written in the same directory as the output file.")
        nx.draw(g1)



if __name__ == '__main__':
    network_sum()

