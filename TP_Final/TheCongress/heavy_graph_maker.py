import networkx as nx
from itertools import combinations


class HeavyGraphMaker:

    DEFINED_WEIGHTS = {
        ('AFIRMATIVO', 'AFIRMATIVO'): 1,
        ('AFIRMATIVO', 'NEGATIVO'): -1,
        ('AFIRMATIVO', 'ABSTENCION'): -1,
        ('AFIRMATIVO', 'AUSENTE'): 0,

        ('NEGATIVO', 'AFIRMATIVO'): -1,
        ('NEGATIVO', 'NEGATIVO'): 1,
        ('NEGATIVO', 'ABSTENCION'): -1,
        ('NEGATIVO', 'AUSENTE'): -1,

        ('ABSTENCION', 'AFIRMATIVO'): -1,
        ('ABSTENCION', 'NEGATIVO'): -1,
        ('ABSTENCION', 'ABSTENCION'): 1,
        ('ABSTENCION', 'AUSENTE'): 0,

        ('AUSENTE', 'AFIRMATIVO'): 0,
        ('AUSENTE', 'NEGATIVO'): 0,
        ('AUSENTE', 'ABSTENCION'): 0,
        ('AUSENTE', 'AUSENTE'): 0

        }

    ##Ponderar

    def __init__(self, congress, config = None):

        self.congress = congress
        self.weights = HeavyGraphMaker.DEFINED_WEIGHTS if not config else self._load_config(config)


    def create_year_network(self, year):
        network = nx.Graph()
        representatives = self.congress.get_yearly_representatives(year)
        votings = self.congress.votings[year]
        network.add_nodes_from(representatives)
        attr_dict = {repr: repr.get_attributes(year) for repr in representatives}
        nx.set_node_attributes(network, attr_dict)

        for repr_1, repr_2 in combinations(representatives, 2):
            weight = self._define_weight(repr_1, repr_2, votings)
            network.add_edge(repr_1, repr_2, weight = weight)

        return network


    def _define_weight(self, repr_1, repr_2, votings):
        ###TODO: si la config dice que 2/3 vale +++
        return sum([self.weights[(repr_1.votes.get(voting, 'AUSENTE'), repr_2.votes.get(voting, 'AUSENTE'))]
                    for voting in votings])

    def _load_config(self, config):
        raise NotImplementedError
