# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 16:26:07 2020

@author: Luna
"""

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations


def enlaces_por_sesion(df):
    #itero la red segun la sesion (asunto)
    numero_sesiones = np.arange(min(df['asuntoId']),max(df['asuntoId'])+1)
    dict_sesiones = {}

    for i in numero_sesiones:
        sesion_i = df[df['asuntoId'] == i]
        dict_sesiones[i] = {}
        
        #agrupo segun el voto (0 = Afirmativo, 1 = Negativo, 2 = Abstención, 3 = Ausente)
        #los ausentes no me interesan
        
        afirmativo_sesion_i = sesion_i[sesion_i['voto'] == 1]
        negativo_sesion_i = sesion_i[sesion_i['voto'] == 2]
        abstencion_sesion_i = sesion_i[sesion_i['voto'] == 3]
        
        #print(afirmativo_sesion_i,negativo_sesion_i,abstencion_sesion_i)
        
        enlaces_afirmativos = list(combinations(afirmativo_sesion_i['nombre'],2))
        enlaces_negativos = list(combinations(negativo_sesion_i['nombre'],2))
        enlaces_abstencion = list(combinations(abstencion_sesion_i['nombre'],2))
        
        #en el diccionario de enlaces no me importa el voto
        dict_sesiones[i] =  enlaces_afirmativos + enlaces_negativos + enlaces_abstencion
        
    return dict_sesiones


def red_pesada(dict_sesiones):
    Red = nx.Graph()
    #cant_sesiones = len(dict_sesiones)
    
    for num_sesion in dict_sesiones: #recorro cada sesion del periodo
        sesion = dict_sesiones[num_sesion]
        for enlace in sesion: #recorro los enlaces de la sesion
        #chequeo si existe el enlace
            if Red.has_edge(enlace[0],enlace[1]): #si existe le 
                Red[enlace[0]][enlace[1]]['weight'] = Red[enlace[0]][enlace[1]]['weight'] + 1
            else:
                Red.add_edge(enlace[0],enlace[1], weight=1)
    return Red

