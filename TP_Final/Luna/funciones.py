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
    nodos = list(dict.fromkeys(list(df['nombre']))) #lista de todos los diputados sin repetir
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
         
        
    return dict_sesiones, nodos



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


def enlaces_por_sesion_desacuerdo(dict_sesiones,nodos): #me devuelve los desacuerdos de cada sesion
    dict_enlaces_desacuerdo = {}
    enlaces_totales = list(combinations(nodos,2))
    
    for num_sesion in dict_sesiones: #reorro cada sesion y devuelvo la diferencia entre las to
        dict_enlaces_desacuerdo[num_sesion] = {}
        enlaces_acuerdo_i = dict_sesiones[num_sesion]
        enlaces_desacuerdo_i = list(set(enlaces_totales) - set(enlaces_acuerdo_i))
        
        dict_enlaces_desacuerdo[num_sesion] = enlaces_desacuerdo_i
        
    return dict_enlaces_desacuerdo

def red_desacuerdos(dict_sesiones_desacuerdo): #red pesada cuyos enlaces son los desacuerdos
    Red = nx.Graph()
    #cant_sesiones = len(dict_sesiones)
    
    for num_sesion in dict_sesiones_desacuerdo: #recorro cada sesion del periodo
        sesion = dict_sesiones_desacuerdo[num_sesion]
        for enlace in sesion: #recorro los enlaces en desacuerdo de la sesion
        #chequeo si existe el enlace
            if Red.has_edge(enlace[0],enlace[1]): #si existe le 
                Red[enlace[0]][enlace[1]]['weight'] = Red[enlace[0]][enlace[1]]['weight'] + 1
            else:
                Red.add_edge(enlace[0],enlace[1], weight=1)
    return Red

def red_pesada_con_desacuerdos(red_acuerdos,red_desacuerdos,nodos):
    Red = nx.Graph()
    enlaces_totales = list(combinations(nodos,2))
    
    for enlace in enlaces_totales: 
        if red_acuerdos.has_edge(enlace[0],enlace[1]): #chequeo si existe el enlace en la red de acuerdos
            
            if red_desacuerdos.has_edge(enlace[0],enlace[1]): #idem con desacuerdos. si no, peso desacuerdos = 0
                peso = red_acuerdos[enlace[0]][enlace[1]]['weight'] - red_desacuerdos[enlace[0]][enlace[1]]['weight']
            else:
                peso = red_acuerdos[enlace[0]][enlace[1]]['weight'] 
            
            Red.add_edge(enlace[0],enlace[1], weight=peso)
            
        elif red_desacuerdos.has_edge(enlace[0],enlace[1]): #si no existe el enlace en la red de acuerdos y si en la de des
            peso = -red_desacuerdos[enlace[0]][enlace[1]]['weight']
            Red.add_edge(enlace[0],enlace[1], weight=peso)
    
    return Red
            
    
    


    
    
    
    
    


