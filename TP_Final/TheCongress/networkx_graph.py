import networkx as nx
import dill
import sys

class RepresentativesGraph:

    @classmethod
    def save_graph_object(cls, grafo, file_name):
        if not sys.getrecursionlimit() == 10000:
            sys.setrecursionlimit(10000)
            print('Recursion limit was set to 10000')
        with open(file_name, 'wb') as file:
            dill.dump(grafo, file)

    @classmethod
    def load_graph_object(cls, file_name):
        with open(file_name, 'rb') as file:
            return dill.load(file)

    def __init__(self, representatives, *years):
        self.representatives = representatives
        self._create_networkx_graph(*years)
        self.years = []
        for year in years:
            self.years.append(year)

    def _create_networkx_graph(self, *years):
        self.graph = nx.Graph()
        self.graph.add_nodes_from(self.representatives)
        if years:
            attr_dict = {repr: self._get_attr(repr, *years) for repr in self.representatives}
            nx.set_node_attributes(self.graph, attr_dict)

    def add_edge(self, node_1, node_2, weight):
        self.graph.add_edge(node_1, node_2, weight = weight)

    def _get_attr(self, repr, *years):
        attr = {}
        for year in years:
            if repr.was_in_year(year):
                attr = repr.get_attributes(year)

        return attr

    def get_sorted_edges_weights(self):
        original_weights = nx.get_edge_attributes(self.graph, 'weight')
        weights = {}
        for k in original_weights.keys():
            weights[tuple(sorted(k, reverse = True))] = original_weights[k]
        return weights

    def get_node_attr(self, attribute):
        return nx.get_node_attributes(self.graph, attribute)

    def get_edge_attr(self, attribute):
        return nx.get_edge_attributes(self.graph, attribute)

    def set_edge_attributes(self, attr_dict, name):
        nx.set_edge_attributes(self.graph, attr_dict, name)

    def set_node_attributes(self, attr_dict, name):
        nx.set_node_attributes(self.graph, attr_dict, name)

    def get_nodes(self):
        return self.graph.nodes()

    def shortest_path(self, initial_node, target_node = None, weight = 'weight'):
        return nx.shortest_path(self.graph, source = initial_node, target = target_node, weight = weight)

    def degree(self, node_id):
        return self.graph.degree(node_id)

    def gigant_component(self):
        components=[self.graph.subgraph(component) for component
                    in sorted(nx.connected_components(self.graph), key=len, reverse=True)]
        gc_networkx = components[0]
        representatives_gc = RepresentativesGraph(list(gc_networkx.nodes()), *self.years)
        representatives_gc.graph = gc_networkx
        size_gc = gc_networkx.number_of_nodes() / self.graph.number_of_nodes()
        return representatives_gc, size_gc

    def remove_edge(self, edge):
        self.graph.remove_edge(edge[0],edge[1])

    def get_edges(self, data = None):
        return self.graph.edges(data = data)

    def add_edges_from_list(self, list_of_edges):
        self.graph.add_edges_from(list_of_edges)

    def copy(self):
        copy = RepresentativesGraph(self.representatives, None)
        copy.graph = self.graph.copy()
        return copy
