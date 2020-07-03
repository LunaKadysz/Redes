from procesador_votaciones import ProcesadorDeVotaciones

import numpy as np
import networkx as nx
from itertools import combinations

 
class HeavyGraphMaker:
    
    def __init__(self):
        #self.edges = self.red_pesada(self,begin,end).edges
        #self.nodes = self._get_congress(begin,end).representatives
        self.nodes = []
        self.enlaces = {}
        
        

    def _get_congress(self, begin, end):
        procesador = ProcesadorDeVotaciones(begin, end, 'data')
        congreso = procesador.procesar()
        return congreso
         
    
    
    def enlaces_por_sesion_acuerdo(self,congreso,begin,end):
        #itero la red segun la sesion (asunto)
        
        anios = np.arange(begin,end+1)
        dict_enlaces = {}
        i= 0
        for anio in anios:
        
            for votacion in congreso.years[anio]:
                dict_enlaces[i] = {}
                
                votos_afirmativos = votacion.votos['AFIRMATIVO']
                votos_negativos = votacion.votos['NEGATIVO']
                votos_abstenciones = votacion.votos['ABSTENCION']
                
                enlaces_afirmativos = list(combinations(votos_afirmativos,2))
                enlaces_negativos = list(combinations(votos_negativos,2))
                enlaces_abstenciones = list(combinations(votos_abstenciones,2))
                
                #en el diccionario de enlaces no me importa el voto
                dict_enlaces[i] =  enlaces_afirmativos + enlaces_negativos + enlaces_abstenciones
                i+=1
                #nodos = list(dict.fromkeys(list(df['nombre']))) #lista de todos los diputados sin repetir
        
        return dict_enlaces



    def red_acuerdos(self,dict_sesiones):
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
    
    
    def enlaces_por_sesion_desacuerdo(self,dict_sesiones,nodos): #me devuelve los desacuerdos de cada sesion
        dict_enlaces_desacuerdo = {}
        enlaces_totales = list(combinations(nodos,2))
        
        for num_sesion in dict_sesiones: #reorro cada sesion y devuelvo la diferencia entre las to
            dict_enlaces_desacuerdo[num_sesion] = {}
            enlaces_acuerdo_i = dict_sesiones[num_sesion]
            enlaces_desacuerdo_i = list(set(enlaces_totales) - set(enlaces_acuerdo_i))
            
            dict_enlaces_desacuerdo[num_sesion] = enlaces_desacuerdo_i
            
        return dict_enlaces_desacuerdo
    
    def red_desacuerdos(self,dict_sesiones_desacuerdo): #red pesada cuyos enlaces son los desacuerdos
        Red = nx.Graph()
        
        for num_sesion in dict_sesiones_desacuerdo: #recorro cada sesion del periodo
            sesion = dict_sesiones_desacuerdo[num_sesion]
            for enlace in sesion: #recorro los enlaces en desacuerdo de la sesion
            #chequeo si existe el enlace
                if Red.has_edge(enlace[0],enlace[1]): #si existe le 
                    Red[enlace[0]][enlace[1]]['weight'] = Red[enlace[0]][enlace[1]]['weight'] + 1
                else:
                    Red.add_edge(enlace[0],enlace[1], weight=1)
        return Red
    
    def red_pesada(self,begin,end):
        Red = nx.Graph()
        congreso = self._get_congress(begin,end)
        nodos = congreso.representatives
        
        dict_enlaces_acuerdo = self.enlaces_por_sesion_acuerdo(congreso,begin,end) #c
        red_acuerdos = self.red_acuerdos(dict_enlaces_acuerdo)
        
        dict_enlaces_desacuerdo = self.enlaces_por_sesion_desacuerdo(dict_enlaces_acuerdo,nodos)
        red_desacuerdos = self.red_desacuerdos(dict_enlaces_desacuerdo)
        
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
        #if save:
         #   disparity_filter.save_graph(Red, f'Red_desacuerdos')
        
        return Red
    
       
    
    
