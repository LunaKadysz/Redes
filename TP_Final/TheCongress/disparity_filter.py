class DisparityFilter:

    MAX_ALPHA = 2


    def __init__(self, network, max_alpha = None):

        self.network = network
        self.max_alpha = DisparityFilter.MAX_ALPHA if not max_alpha else max_alpha

    def _disparity_integral (self,x, k):
        """
        calculate the definite integral in the disparity filter
        \int (1 - x)^(k - 2)
        """
        return (- (1.0 - x)**(k - 1) / ((k - 1.0)))


    def _get_disparity_significance (self,norm_weight, degree):
        """
        calculate the alpha for the disparity filter
        """
        return 1.0 - ((degree - 1.0) * (self._disparity_integral(norm_weight, degree) - self._disparity_integral(0.0, degree)))


    def _get_node_strength(self, node_id, weights):
        strength = 0
        for edge, weight in weights.items():
            if node_id in edge:
                strength += weight
        return strength

    def _get_norm_weight(self, strength, weight, degree):
        if strength == 0:
            strength = 1
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
                    norm_weight = self._get_norm_weight(strength, weight, degree)

                if degree > 1:
                    alpha = self._get_disparity_significance(norm_weight, degree)
                    old_alpha = alphas[edge]
                    if old_alpha > alpha:
                        alphas[edge] = alpha

                else:
                    alphas[edge] = 0

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


    def cut_graph(self, GC_limit_size = 0.8):
        alpha_measures, weights = self._get_sorted_alphas()
        gc, size_gc = self.network.gigant_component()

        i = 0
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

        return self.network
