import decimal
decimal.getcontext().prec = 100
from scipy import integrate
import numpy as np

class NewDisparityFilter():

    MAX_ALPHA = 1

    def __init__(self, network, max_alpha = None):

        self.network = network
        self.max_alpha = NewDisparityFilter.MAX_ALPHA if not max_alpha else max_alpha

    def _get_network_alphas(self):
        weights = self.network.get_sorted_edges_weights()
        alphas = {e: self.max_alpha for e in weights.keys()}

        for node_id in self.network.get_nodes():
            degree = self.network.degree(node_id)
            strength = self._get_node_strength(node_id, weights)

            for edge, weight in weights.items():
                if node_id in edge: #para los edges del nodo
                    p_ij = self._get_norm_weight(strength, weight, degree)

                if degree > 1:
                    alpha = self._get_disparity_parameter(p_ij, degree)
                    old_alpha = alphas[edge]
                    if old_alpha > alpha:
                        alphas[edge] = alpha

        return alphas

    def alpha_cut(self, alpha_t = 0.05):
        alphas_dict = self._get_network_alphas()
        total_edges = len(alphas_dict)
        print(f'The graph has {total_edges} edges')
        min_alpha = min(alphas_dict.values())
        max_alpha = max(alphas_dict.values())
        print(f'Max alpha is {max_alpha}, min alpha is {min_alpha}')

        if alpha_t < min_alpha:
            print(f'That limit is impossible! Min alpha is {min_alpha}')
            return
        if alpha_t > max_alpha:
            print(f'That limit is impossible! Max alpha is {max_alpha}')
            return

        i = 0
        for edge, alpha in alphas_dict.items():
            if alpha > alpha_t:
                self.network.remove_edge(edge)
                i += 1
                print(f'Enlaces sacados: {i}')


        print(f'{i} edges deleted, {total_edges - i} left')
        _, size_gc = self.network.gigant_component()
        print(f'Gigant component is {size_gc} of the total')
        return self.network


    def _get_node_strength(self, node_id, weights):
        strength = 0
        for edge, weight in weights.items():
            if node_id in edge:
                strength += np.abs(weight)
        return strength

    def _get_norm_weight(self, strength, weight, degree):
        norm_weight = np.abs(weight) / strength
        if  norm_weight == 1.0: #no diverja la integral
            return norm_weight - 0.01
        return norm_weight

    def _get_disparity_parameter(self, norm_weight, degree):
        return (1 - norm_weight) ** (degree - 1)
