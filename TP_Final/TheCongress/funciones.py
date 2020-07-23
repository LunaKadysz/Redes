# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 13:43:43 2020

@author: Luna
"""

import community as community_louvain # Importo el paquete que instalé en la línea de arriba
import igraph as ig # Importo igraph
import networkx as nx # Para redes en general
import leidenalg as la

def save_graph_object(grafo, file_name):
    with open(file_name, 'wb') as file:
        dill.dump(grafo, file)
        
def load_graph_object(file_name):
    with open(file_name, 'rb') as file:
        return dill.load(file)
    
def convertir_particion_igraph_a_diccionario(Red_igraph,particion_igraph):
  particion_dict = {}
  for cluster in range(len(particion_igraph)):
    for nodo in Red_igraph.vs(particion_igraph[cluster])['name']:
      particion_dict.update({nodo:cluster})
  return particion_dict


#devuelve una lista de n colores hex
import random
def colores_hex(n):
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])for i in range(n)]
    return color


# devuelve particiones con Edge Betweenness	
#The edge weights. Supply NULL to omit edge weights. By default the ‘weight’ edge attribute is used, if it is present.
#Edge weights are used to calculate weighted edge betweenness.
#This means that edges are interpreted as distances, not as connection strengths
def edge_betweenness(Red_recableada,w): 
  Red_igraph = ig.Graph.TupleList(Red_recableada.edges(), directed=False) #la paso a igraph
  dendograma_edge_betweenness = Red_igraph.community_edge_betweenness(weights=w)
  particiones_edge_betweenness = dendograma_edge_betweenness.as_clustering()
  dict_particiones_edge_betweenness = convertir_particion_igraph_a_diccionario(Red_igraph,particiones_edge_betweenness)
  return dict_particiones_edge_betweenness


#devuelve particiones con Fast Greedy
# If not NULL, then a numeric vector of edge weights. The length must match the number of edges in the graph.
# By default the ‘weight’ edge attribute is used as weights.
# If it is not present, then all edges are considered to have the same weight. 
# Larger edge weights correspond to stronger connections.
def fast_greedy(Red_recableada,w):
  Red_igraph = ig.Graph.TupleList(Red_recableada.edges(), directed=False) #la paso a igraph
  dendograma_fast_greedy = Red_igraph.community_fastgreedy(weights=w)
  particiones_fast_greedy = dendograma_fast_greedy.as_clustering()
  dict_particiones_fast_greedy = convertir_particion_igraph_a_diccionario(Red_igraph,particiones_fast_greedy)
  return dict_particiones_fast_greedy


#particiones con Louvline
#https://en.wikipedia.org/wiki/Louvain_modularity
def louvile(Red_recableada,w):
  dict_particiones_louvline = community_louvain.best_partition(Red_recableada, weight=w)
  return dict_particiones_louvline

def leiden1(red,w):
    Red_igraph = ig.Graph.TupleList(red.edges(), directed=False)
    ig_partition = la.find_partition(Red_igraph,la.ModularityVertexPartition,weights=w)
    dict_particiones_leiden1 = convertir_particion_igraph_a_diccionario(Red_igraph,ig_partition)
    return dict_particiones_leiden1


#particiones con infomap
#e.weights	
#If not NULL, then a numeric vector of edge weights. The length must match the number of edges in the graph.
#By default the ‘weight’ edge attribute is used as weights.
#If it is not present, then all edges are considered to have the same weight.
#Larger edge weights correspond to stronger connections.
def infomap(Red_recableada,w):
  Red_igraph = ig.Graph.TupleList(Red_recableada.edges(), directed=False) #la paso a igraph
  particiones_infomap = Red_igraph.community_infomap()
  dict_particiones_infomap = convertir_particion_igraph_a_diccionario(Red_igraph,particiones_infomap)
  return dict_particiones_infomap


