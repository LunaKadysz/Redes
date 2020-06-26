# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
voto = pd.read_csv('../otrosDatasets/votaciones-diputados.csv')
bloque = pd.read_csv('../otrosDatasets/bloques-diputados.csv')

voto=voto[["diputadoId","bloqueId"]]
voto=voto.drop_duplicates()

diputados=voto["diputadoId"].drop_duplicates()


#In [17]: voto[voto["diputadoId"]==70]
#Out[17]: 
#       diputadoId  bloqueId
#1              70        80
#15366          70       128
#26120          70       100

enlaces_partidos=[]
for diputado in diputados:
    partidos_a_enlazar=voto[voto["diputadoId"]==diputado]["bloqueId"].to_numpy()
    G=nx.complete_graph(partidos_a_enlazar)
    for edge in G.edges():
        enlaces_partidos.append(tuple(sorted(edge)))
    del G,partidos_a_enlazar

count_enlaces= {i:enlaces_partidos.count(i) for i in enlaces_partidos}

enlaces_partidos_pesados=[]
for enlace in count_enlaces:
    enlaces_partidos_pesados.append((enlace[0],enlace[1],count_enlaces[enlace]))

Red=nx.Graph()
#Red.add_nodes_from(partidos)
Red.add_weighted_edges_from(enlaces_partidos_pesados)
#
#G.add_weighted_edges_from([(0, 1, 3.0), (1, 2, 7.5)])
#nx.draw(Red,node_size = 40)
#plt.savefig('plotgraph.png', dpi=300, bbox_inches='tight')
#plt.show()
lista_componentes=[Red.subgraph(componente) for componente in sorted(nx.connected_components(Red), key=len, reverse=True)]
plt.figure()
nx.draw(lista_componentes[0],node_size = 40)
plt.savefig('plotgraphCG.png', dpi=300, bbox_inches='tight')
plt.title('Componente Gigante')

for i in range(len(lista_componentes)):
    nodes=lista_componentes[i].nodes()
    print(f"Componente {i}:")
    for node in nodes:
        nombre=bloque[bloque["bloqueId"]==node].iloc[0]["bloque"]
        print(f"\t{nombre}")
