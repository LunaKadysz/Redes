# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 12:47:32 2020

@author: Luna
"""
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import funciones as f

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

anios_elecciones_legislativas = np.arange(1995,2018,2)

fig, axs = plt.subplots(3, 4, figsize=(15,15))
axs = axs.flatten()

for i,anio in enumerate(anios_elecciones_legislativas):
    df_periodo = pd.concat([df[df['ano'] == anio],df[df['ano'] == anio+1]]) #busco los datos de un periodo (2 anios)
    dict_enlaces_periodo_i = f.enlaces_por_sesion(df_periodo) #funcion que devuelve los enlaces en dict
    red_periodo_i = f.red_pesada(dict_enlaces_periodo_i)
    posiciones = nx.kamada_kawai_layout(red_periodo_i)
    nx.draw_networkx_nodes(red_periodo_i,node_size= 100, ax = axs[i],pos= posiciones)
    nx.draw_networkx_edges(red_periodo_i, ax = axs[i], width=1.0, alpha=0.2,pos=posiciones)

        





