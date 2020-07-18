#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 00:26:26 2020

@author: carolina
"""

from procesador_votaciones import ProcesadorDeVotaciones
from heavy_graph_maker import HeavyGraphMaker

begin = 2019
end = 2019
procesador = ProcesadorDeVotaciones(begin,end, 'data')
congress = procesador.procesar()
congress.validate()
network= HeavyGraphMaker(congress).create_year_network(2019)
from new_disparity_filter import NewDisparityFilter
network_cut2 =  NewDisparityFilter(network).alpha_cut()