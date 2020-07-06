from networkx_graph import RepresentativesGraph
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

    # PONDERATE = 1

    def __init__(self, congress, config = None):

        self.congress = congress
        self.weights = HeavyGraphMaker.DEFINED_WEIGHTS if not config else self._load_config(config)


    def create_year_network(self, year):

        representatives = self.congress.get_yearly_representatives(year)
        votings = self.congress.votings[year]
        network = RepresentativesGraph(representatives, year)

        for repr_1, repr_2 in combinations(representatives, 2):
            weight = self._define_weight(repr_1, repr_2, votings)
            network.add_edge(repr_1, repr_2, weight)

        return network

    def create_voting_network(self, voting):

        representatives = voting.get_voters()
        network = RepresentativesGraph(representatives, year)

        for repr_1, repr_2 in combinations(representatives, 2):
            weight = self._define_weight(repr_1, repr_2, [voting])
            network.add_edge(repr_1, repr_2, weight)

        return network



    def _define_weight(self, repr_1, repr_2, voting_list):
        ###TODO: si la config dice que 2/3 vale +++
        #le hacemos get y si no lo encuentra lo toma ausente (por si se murio o renuncio)
        return sum([self.weights[(repr_1.votes.get(voting, 'AUSENTE'), repr_2.votes.get(voting, 'AUSENTE'))]
                    for voting in voting_list])

    def _load_config(self, config):
        raise NotImplementedError
