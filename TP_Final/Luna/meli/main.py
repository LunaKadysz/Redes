from procesador_votaciones import ProcesadorDeVotaciones
from heavy_graph_maker import HeavyGraphMaker
from the_congress import TheCongress
from voting import Voting
from itertools import combinations

procesador = ProcesadorDeVotaciones(2017, 2018, 'data')
congress = procesador.procesar()

lista = []
anios = np.array([2017,2018])

#for anio in anios:
#    for i,vote in enumerate(congress.years[anio]):
#        
#        votos_afirmativos = vote.votos['AFIRMATIVO']
#        votos_negativos = vote.votos['NEGATIVO']
#        votos_abstenciones = vote.votos['ABSTENCION']
#        
#    lista.append(congress.representatives)
# a = list(dict.fromkeys(lista)))
#    
#print(len(lista[1]))

grafo = HeavyGraphMaker()
red = grafo.red_pesada(1993,1994)




