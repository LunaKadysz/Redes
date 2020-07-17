import networkx as nx
import numpy as np
from scipy import integrate
import decimal
decimal.getcontext().prec = 100
from networkx_graph import RepresentativesGraph

class DisparityFilter2:

    MAX_ALPHA = 2
    
    def __init__(self, network, max_alpha = None):

        self.network = network
        self.max_alpha = DisparityFilter2.MAX_ALPHA if not max_alpha else max_alpha


    def disparity_filter(self, weight='weight'):
        ''' Compute significance scores (alpha) for weighted edges in G as defined in Serrano et al. 2009
            Args
                G: Weighted NetworkX graph
            Returns
                Weighted graph with a significance score (alpha) assigned to each edge
            References
                M. A. Serrano et al. (2009) Extracting the Multiscale backbone of complex weighted networks. PNAS, 106:16, pp. 6483-6488.
        '''
        B = nx.Graph()
        for u in self.network:
            k = len(self.network[u])
            if k > 1:
                sum_w = sum(np.absolute(self.network[u][v][weight]) for v in self.network[u])
                for v in self.network[u]:
                    w = self.network[u][v][weight]
                    p_ij = float(np.absolute(w))/sum_w
                    alpha_ij = 1 - (k-1) * integrate.quad(lambda x: (1-x)**(k-2), 0, p_ij)[0]
                    B.add_edge(u, v, weight = w, alpha=float('%.4f' % alpha_ij))
        return B
    
    def disparity_filter_alpha_cut(self,weight='weight',alpha_t=0.4):
        ''' Performs a cut of the graph previously filtered through the disparity_filter function.
            
            Args
            ----
            G: Weighted NetworkX graph
            
            weight: string (default='weight')
                Key for edge data used as the edge weight w_ij.
                
            alpha_t: double (default='0.4')
                The threshold for the alpha parameter that is used to select the surviving edges.
                It has to be a number between 0 and 1.
                

                
                
            Returns
            -------
            B: Weighted NetworkX graph
                The resulting graph contains only edges that survived from the filtering with the alpha_t threshold
        
            References
            ---------
            .. M. A. Serrano et al. (2009) Extracting the Multiscale backbone of complex weighted networks. PNAS, 106:16, pp. 6483-6488.
        '''    
        
        B = self.disparity_filter()
        G = nx.Graph()
        for u, v, w in B.edges(data=True):
            try:
                alpha = w['alpha']
            except KeyError: #there is no alpha, so we assign 1. It will never pass the cut
                alpha = 1
                    
            if alpha<alpha_t:
                G.add_edge(u,v, weight=w[weight])
        return G
                