from procesador_votaciones import ProcesadorDeVotaciones
from heavy_graph_maker import HeavyGraphMaker

begin = 2019
end = 2019
procesador = ProcesadorDeVotaciones(begin,end, 'data')
congress = procesador.procesar()
congress.validate()

#Defino configs con solo pesos positivos y con solo pesos negativos para desarmar en dos redes luego
#config= HeavyGraphMaker(congress).weights
config={
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
Positive_config=config.copy()
Negative_config=config.copy()

for item in Positive_config:
    if Positive_config[item]==-1:
        Positive_config[item]=0
        
for item in Negative_config:
    if Negative_config[item]==1:
        Negative_config[item]=0
    if Negative_config[item]==-1:
        Negative_config[item]=1
        
#network= HeavyGraphMaker(congress).create_year_network(2019)
network_pos = HeavyGraphMaker(congress, config=Positive_config).create_year_network(2019)
network_neg = HeavyGraphMaker(congress, config=Negative_config).create_year_network(2019)

import networkx as nx
# =============================================================================
# from disparity_filter import DisparityFilter
# #network_cut=DisparityFilter(network).cut_graph(alpha_limit=0.05)
# 
# network_pos_cut= DisparityFilter(network_pos).cut_graph(alpha_limit=0.05)
# network_neg_cut= DisparityFilter(network_neg).cut_graph(alpha_limit=0.05)
# 
# =============================================================================
from new_disparity_filter import NewDisparityFilter
#network_cut2=NewDisparityFilter(network).alpha_cut()
network_pos_cut= NewDisparityFilter(network_pos).alpha_cut()
network_neg_cut= NewDisparityFilter(network_neg).alpha_cut()