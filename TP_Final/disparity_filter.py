######################################################################
## disparity filter for extracting the multiscale backbone of
## complex weighted networks
from networkx.readwrite import json_graph
import json
import networkx as nx
import sys

MAX_ALPHA = 2 #alpha is normalized

def disparity_integral (x, k):
    """
    calculate the definite integral in the disparity filter
    \int (1 - x)^(k - 2)
    """
    assert x != 1.0, "x == 1.0"
    assert k != 1.0, "k == 1.0"
    return (- (1.0 - x)**(k - 1) / ((k - 1.0)))


def get_disparity_significance (norm_weight, degree):
    """
    calculate the alpha for the disparity filter
    """
    return 1.0 - ((degree - 1.0) * (disparity_integral(norm_weight, degree) - disparity_integral(0.0, degree)))


def disparity_filter (graph):
    """
    implements a disparity filter, based on multiscale backbone networks
    https://arxiv.org/pdf/0904.2389.pdf
    """
    alpha_measures = {}

    for node_id in graph.nodes():
        node = graph.nodes()[node_id]
        degree = graph.degree(node_id)
        strength = 0.0

        for id0, id1 in graph.edges(nbunch=[node_id]): #edges del nodo
            edge = graph[id0][id1] #uno es node_id??
            strength += edge["weight"] #ejercicio: una sola linea

            """
            streng = sum([(graph[edge[0],edge[1]])['weight'] for edge in  graph.edges(nbunch=[node_id])])
            """

        node["strength"] = strength

        for edge in graph.edges(nbunch=[node_id]):
            edge_data = graph[edge[0]][edge[1]]
            norm_weight = edge_data["weight"] / strength
            edge_data["norm_weight"] = norm_weight

            if degree > 1:
                try:
                    if norm_weight == 1.0:
                        norm_weight -= 0.0001 #no rompa la integral

                    alpha = get_disparity_significance(norm_weight, degree)
                except AssertionError:
                    print(f'Error with disparity {node}')

                edge_data["alpha"] = alpha
                sorted_edge = tuple(sorted(edge))
                if alpha_measures.get(sorted_edge, MAX_ALPHA) > alpha:
                    alpha_measures[sorted_edge] = alpha
            else:
                edge_data["alpha"] = 0.0
    return alpha_measures

def remove_highest_alpha(graph, sorted_alphas):
    edge, _ = sorted_alphas[0]
    edge_data = graph[edge[0]][edge[1]]
    graph.remove_edge(edge[0],edge[1])
    components=[graph.subgraph(component) for component
                in sorted(nx.connected_components(graph), key=len, reverse=True)]
    GC = components[0]
    size_GC = GC.number_of_nodes() / graph.number_of_nodes()
    del(sorted_alphas[0])
    return size_GC, sorted_alphas, edge, edge_data

def cut_graph(graph, GC_limit_size = 0.8, save = True, name = 'grafo'):
    if save:
        save_graph(graph, f'{name}_original')
    alpha_measures_dict = disparity_filter(graph)
    sorted_by_alphas = sorted(alpha_measures_dict.items(), key=lambda x: x[1], reverse=True)
    components=[graph.subgraph(component) for component
                in sorted(nx.connected_components(graph), key=len, reverse=True)]
    GC = components[0]
    size_GC = GC.number_of_nodes() / graph.number_of_nodes()

    while size_GC > GC_limit_size:
        new_size_GC, new_sorted_alphas, edge_removed, edge_data_removed = remove_highest_alpha(graph, sorted_by_alphas)
        sorted_alphas = new_sorted_alphas
        size_GC = new_size_GC
     #el while termina cuando mi GC es menor, entonces vuelvo a agregar edge
    graph.add_edge(edge_removed[0], edge_removed[1], **edge_data_removed)
    if save:
        save_graph(graph, f'{name}_recortado')
    return graph

def save_graph(graph, version):
    data = json_graph.node_link_data(graph)
    with open(f'json_{version}.txt', 'w') as outfile:
        json.dump(data, outfile)
