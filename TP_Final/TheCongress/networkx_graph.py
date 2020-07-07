import networkx as nx

class RepresentativesGraph():

    def __init__(self, representatives, year):
        self.representatives = representatives
        self._create_networkx_graph(year)

    def _create_networkx_graph(self, year):
        self.graph = nx.Graph()
        self.graph.add_nodes_from(self.representatives)
        attr_dict = {repr: repr.get_attributes(year) for repr in self.representatives}
        nx.set_node_attributes(self.graph, attr_dict)

    def add_edge(self, node_1, node_2, weight):
        self.graph.add_edge(node_1, node_2, weight = weight)

    def get_sorted_edges_weights(self):
        original_weights = nx.get_edge_attributes(self.graph, 'weight')
        weights = {}
        for k in original_weights.keys():
            weights[tuple(sorted(k, reverse = True))] = original_weights[k]
        return weights

    def get_nodes(self):
        return self.graph.nodes()

    def degree(self, node_id):
        return self.graph.degree(node_id)

    def gigant_component(self):
        components=[self.graph.subgraph(component) for component
                    in sorted(nx.connected_components(self.graph), key=len, reverse=True)]
        gc = components[0]
        size_gc = gc.number_of_nodes() / self.graph.number_of_nodes()
        return gc, size_gc

    def remove_edge(self, edge):
        self.graph.remove_edge(edge[0],edge[1])
