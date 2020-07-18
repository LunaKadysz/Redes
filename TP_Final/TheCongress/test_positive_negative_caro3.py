#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 01:13:19 2020

@author: carolina
"""

import networkx as nx
from procesador_votaciones import ProcesadorDeVotaciones
from heavy_graph_maker import HeavyGraphMaker

begin = 2019
end = 2019
procesador = ProcesadorDeVotaciones(begin,end, 'data')
congress = procesador.procesar()
congress.validate()

#Defino configs con solo pesos positivos y con solo pesos negativos para desarmar en dos redes luego
config= HeavyGraphMaker(congress).weights
Positive_config=config
Negative_config=config

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

from new_disparity_filter import NewDisparityFilter
#network_cut2=NewDisparityFilter(network).alpha_cut()
network_pos_cut= NewDisparityFilter(network_pos).alpha_cut()
network_neg_cut= NewDisparityFilter(network_neg).alpha_cut()