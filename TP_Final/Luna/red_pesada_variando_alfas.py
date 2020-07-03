# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 15:45:54 2020

@author: Luna
"""


import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import funciones as f
import disparity_filter

diputado = pd.read_csv('../otrosDatasets/diputados.csv')
voto = pd.read_csv('../otrosDatasets/votaciones-diputados.csv')
bloque = pd.read_csv('../otrosDatasets/bloques-diputados.csv')
asuntos = pd.read_csv('../otrosDatasets/asuntos-diputados.csv')

voto_df = pd.DataFrame(data=voto)
diputado_df = pd.DataFrame(data=diputado)
bloque_df = pd.DataFrame(data=bloque)

#elimino las filas nans y convierto float a nan asi puedo hacer un inner join
diputado_df = diputado_df.dropna(how='all')
diputado_df['diputadoID'] = diputado_df['diputadoID'].apply(np.int64)

#inner join: este data frame es voto y diputado mergeado segun id
df = pd.merge(voto_df, diputado_df, left_on='diputadoId', right_on='diputadoID')
df = pd.merge(df,asuntos,left_on = 'asuntoId',right_on = 'asuntoId')
df = df[df['ano'] == 2017]
alfas = np.arange(60,90,10)

fig, axs = plt.subplots(1, 3, figsize=(20,15))
axs = axs.flatten()

for i,alfa in enumerate(alfas):

    axs[i].set_title(f'alfa: {alfa}')
    dict_enlaces,nodos = f.enlaces_por_sesion(df) #funcion que devuelve los enlaces en dict
    dict_sesiones_desacuerdo = f.enlaces_por_sesion_desacuerdo(dict_enlaces,nodos)
    red_acuerdos = f.red_pesada(dict_enlaces)
    red_desacuerdos = f.red_desacuerdos(dict_sesiones_desacuerdo)
    red_final_i = f.red_pesada_con_desacuerdos(red_acuerdos,red_desacuerdos,nodos)

    red_cortada = disparity_filter.cut_graph(red_final_i, save = True, name=f'grafo {alfa}')

    posiciones = nx.kamada_kawai_layout(red_cortada,weight='norm_weight')
    #posiciones =nx.spectral_layout(red_periodo_i, weight='weight')

    nx.draw_networkx_nodes(red_cortada,node_size= 50, ax = axs[i],pos= posiciones,node_color='red')
    nx.draw_networkx_edges(red_cortada, ax = axs[i], alpha=0.1,pos=posiciones,edge_color='salmon')