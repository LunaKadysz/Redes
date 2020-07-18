from networkx_graph import RepresentativesGraph
from itertools import combinations
import numpy as np


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

    # PONDERATE = 1

    def __init__(self, congress, config = None):

        self.congress = congress
        self.weights = HeavyGraphMaker.DEFINED_WEIGHTS if not config else self._load_config(config)


    def move_weights(self, network, *years):
        old_weights = network.get_sorted_edges_weights()
        min_weight = min(old_weights.values())
        print(f'Min weight was {min_weight}')
        total_votes = 0 #Esto es por si queremos normalizar
        for year in years:
            total_votes += len(self.congress.votings[year])
        new_weights = {e: (w + np.abs(min_weight) + 1) / total_votes for e,w in old_weights.items()}
        network.set_edge_attributes(new_weights, 'weight')


    def create_year_network(self, *years, move_zero = None, positive = None, negative = None):
        representatives = set()
        votings = []
        for year in years:
            votings.extend(self.congress.votings[year])
            representatives.update(self.congress.get_yearly_representatives(year))

        network = RepresentativesGraph(representatives, years)
        for repr_1, repr_2 in combinations(representatives, 2):
            weight = self._define_weight(repr_1, repr_2, votings, *years)
            if positive and weight > 0:
                network.add_edge(repr_1, repr_2, weight)
            if negative and weight < 0:
                network.add_edge(repr_1, repr_2, weight)
            if not negative and not positive:
                network.add_edge(repr_1, repr_2, weight)

        if move_zero:
            self.move_weights(network, *years)

        return network


    def create_voting_network(self, voting, positive = None, negative = None):

        representatives = voting.get_voters()
        network = RepresentativesGraph(representatives, year)

        for repr_1, repr_2 in combinations(representatives, 2):
            weight = self._define_weight(repr_1, repr_2, [voting])
            network.add_edge(repr_1, repr_2, weight)

        return network


    def _define_weight(self, repr_1, repr_2, voting_list, *years):
        ###TODO: si la config dice que 2/3 vale +++
        #le hacemos get y si no lo encuentra lo toma ausente (por si se murio o renuncio)
        return sum([self.weights[(repr_1.votes.get(voting, 'AUSENTE'), repr_2.votes.get(voting, 'AUSENTE'))]
                    for voting in voting_list])

    def _load_config(self, config):
        return config
