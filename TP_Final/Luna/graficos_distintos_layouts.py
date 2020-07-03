# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 19:47:06 2020

@author: Luna
"""

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import funciones as f
import json

original = open('grafos/json_grafo 80_original.txt') 
data_o = json.load(original) 

cortada = open('grafos/json_grafo 80_recortado.txt') 
data_r = json.load(cortada) 

#armo red original
Red_original = nx.Graph()
for edge in data_o['links']:
    Red_original.add_edge(edge['source'],edge['target'], weight=edge['weight'])
    
Red_cortada = nx.Graph()
for edge in data_r['links']:
    Red_cortada.add_edge(edge['source'],edge['target'], weight=edge['norm_weight'])    




layouts = [#nx.rescale_layout,
           nx.shell_layout,
           nx.spring_layout,
           nx.spectral_layout,
           #nx.planar_layout,
           nx.fruchterman_reingold_layout]
           #nx.spiral_layout]

fig, axs = plt.subplots(2, 4, figsize=(15,20))

for i,layout in enumerate(layouts):

    posiciones_original = layout(Red_original)
    posiciones_cortada = layout(Red_cortada)
    
    #grafico red original
    nx.draw_networkx_nodes(Red_original,node_size= 50, ax = axs[0][i],pos= posiciones_original,node_color='red')
    nx.draw_networkx_edges(Red_original, ax = axs[0][i], alpha=0.1,pos=posiciones_original,edge_color='salmon')
    
    #grafico red cortada
    nx.draw_networkx_nodes(Red_cortada,node_size= 50, ax = axs[1][i],pos= posiciones_cortada,node_color='mediumseagreen')
    nx.draw_networkx_edges(Red_cortada, ax = axs[1][i], alpha=0.1,pos=posiciones_cortada,edge_color='mediumaquamarine')   

    
