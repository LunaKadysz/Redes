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
import disparity_filter as filter

diputado = pd.read_csv('./otrosDatasets/diputados.csv')
voto = pd.read_csv('./otrosDatasets/votaciones-diputados.csv')
bloque = pd.read_csv('./otrosDatasets/bloques-diputados.csv')
asuntos = pd.read_csv('./otrosDatasets/asuntos-diputados.csv')

voto_df = pd.DataFrame(data=voto)
diputado_df = pd.DataFrame(data=diputado)
bloque_df = pd.DataFrame(data=bloque)

#elimino las filas nans y convierto float a nan asi puedo hacer un inner join
diputado_df = diputado_df.dropna(how='all')
diputado_df['diputadoID'] = diputado_df['diputadoID'].apply(np.int64)

#inner join: este data frame es voto y diputado mergeado segun id
df = pd.merge(voto_df, diputado_df, left_on='diputadoId', right_on='diputadoID')
df = pd.merge(df,asuntos,left_on = 'asuntoId',right_on = 'asuntoId')

anios_elecciones_legislativas = np.insert(np.arange(1994,2019,2),0,1993) #anios pares + 1995

for i,anio in enumerate(anios_elecciones_legislativas):
    fig, ax = plt.subplots()
    if anio == 1993:
         df_periodo = df[df['ano'] == anio]
         ax.set_title(f'Periodo {anio}')
    if anio == 2018:
        df_periodo = df[df['ano'] == anio]
        ax.set_title(f'Periodo {anio}')

    else:
        df_periodo = pd.concat([df[df['ano'] == anio],df[df['ano'] == anio+1]]) #busco los datos de un periodo (2 anios)
        ax.set_title(f'Periodo {anio} - {anio+1}')

    dict_enlaces_periodo_i = f.enlaces_por_sesion(df_periodo) #funcion que devuelve los enlaces en dict
    red_periodo_i = f.red_pesada(dict_enlaces_periodo_i)
    #posiciones = nx.(red_periodo_i)
    red_cortada_i = filter.cut_graph(red_periodo_i)
    #posiciones =nx.kamada_kawai_layout(red_cortada_i)

    nx.draw_networkx_nodes(red_cortada_i,node_size= 50, ax = ax,pos= posiciones,node_color='red')
    nx.draw_networkx_edges(red_cortada_i, ax = ax, alpha=0.1,pos=posiciones,edge_color='salmon')
    print(f'{anio} listooooo!')
    plt.savefig(f'grafo_cortado_kamada_{anio}.png')
