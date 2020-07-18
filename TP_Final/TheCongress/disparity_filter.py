import decimal
decimal.getcontext().prec = 100
import numpy as np
from scipy import integrate

class DisparityFilter:

    MAX_ALPHA = 2


    def __init__(self, network, max_alpha = None):

        self.network = network
        self.max_alpha = DisparityFilter.MAX_ALPHA if not max_alpha else max_alpha

    def _get_disparity_parameter(self, norm_weight, degree):
        """
        calculate the alpha DIRECTLY for the disparity filter
        """
        return 1 - (degree - 1) * integrate.quad(lambda x: (1 - x)**(degree - 2), 0, norm_weight)[0]

    def _get_node_strength(self, node_id, weights):
        strength = 0
        for edge, weight in weights.items():
            if node_id in edge:
                strength += weight
        return strength

    def _get_norm_weight(self, strength, weight, degree):
        norm_weight = weight / strength
        if  norm_weight == 1.0: #no diverja la integral
            return norm_weight - 0.01
        return norm_weight

    def _get_network_alphas(self):
        weights = self.network.get_sorted_edges_weights()
        alphas = {k: self.max_alpha for k in weights.keys()}

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

                else:
                    alphas[edge] = 1

        return alphas, weights


    def _get_sorted_alphas(self):
        alphas, weights = self._get_network_alphas()
        sorted_alphas = sorted(alphas.items(), key=lambda x: x[1], reverse=True)
        return sorted_alphas, weights

    def _remove_highest_alpha(self, alphas, weights):
        edge, _ = alphas[0]
        self.network.remove_edge(edge)
        gc, size_gc = self.network.gigant_component()
        del(alphas[0])
        return size_gc, alphas, edge, {'weight': weights[edge]}


    def cut_graph(self, GC_limit_size = None, alpha_limit = None):
        alpha_measures, weights = self._get_sorted_alphas()
        total_edges = len(alpha_measures)
        print(f'The graph has {total_edges} edges')
        print(f'First alpha is {alpha_measures[0][1]}, last one is {alpha_measures[-1][1]}')
        i = 0

        if GC_limit_size:
            gc, size_gc = self.network.gigant_component()
            while size_gc > GC_limit_size:
                new_size_gc, new_sorted_alphas, edge_removed, edge_data_removed = self._remove_highest_alpha(alpha_measures, weights)
                if new_size_gc != size_gc:
                    print(f'Cambio en la GC: de {size_gc} a {new_size_gc}')
                alpha_measures = new_sorted_alphas
                size_gc = new_size_gc
                i += 1
                print(f'Enlaces sacados: {i}')

                 #el while termina cuando mi GC es menor, entonces vuelvo a agregar edge
            self.network.add_edge(edge_removed[0], edge_removed[1], **edge_data_removed)
            #print(f'Next alpha is {alpha_measures[0][1]}')

        if alpha_limit:
            if alpha_limit < alpha_measures[-1][1]:
                print(f'That limit is impossible! Min alpha is {alpha_measures[-1][1]}')
                return
            if alpha_limit > alpha_measures[0][1]:
                print(f'That limit is impossible! Max alpha is {alpha_measures[0][1]}')
                return

            while alpha_measures[0][1] > alpha_limit:
                _, new_sorted_alphas, edge_removed, edge_data_removed = self._remove_highest_alpha(alpha_measures, weights)
                alpha_measures = new_sorted_alphas
                i += 1
                print(f'Enlaces sacados: {i}')

             #el while termina cuando mi GC es menor, entonces vuelvo a agregar edge
            self.network.add_edge(edge_removed[0], edge_removed[1], **edge_data_removed)
        print(f'Enlaces sacados: {i}')
        print(f'{i} edges deleted, {total_edges - i} left')
        print(f'Next alpha is {alpha_measures[0][1]}')

        return self.network
