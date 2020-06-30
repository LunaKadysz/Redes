# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 20:10:15 2020

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

df = df.head(50)


dict_enlaces_periodo,nodos = f.enlaces_por_sesion(df) #funcion que devuelve los enlaces en dict
dict_sesiones_desacuerdo = f.enlaces_por_sesion_desacuerdo(dict_enlaces_periodo,nodos)
red_acuerdos = f.red_pesada(dict_enlaces_periodo)
red_desacuerdos = f.red_desacuerdos(dict_sesiones_desacuerdo)   
red_final = f.red_pesada_con_desacuerdos(red_acuerdos,red_desacuerdos,nodos)


posiciones = nx.spring_layout(red_final)
    #posiciones =nx.spectral_layout(red_periodo_i, weight='weight')

#nx.draw_networkx_nodes(red_final,node_size= 50,pos= posiciones,node_color='red')
#nx.draw_networkx_edges(red_final, alpha=0.1,pos=posiciones,edge_color='salmon')
plt.figure()
nx.draw(red_acuerdos,pos= posiciones)
plt.figure()
nx.draw(red_desacuerdos,pos= posiciones)
plt.figure()
nx.draw(red_final,pos= posiciones)
    