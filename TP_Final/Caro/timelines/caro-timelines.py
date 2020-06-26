# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
from datetime import datetime

diputado = pd.read_csv('./otrosDatasets/diputados.csv')
voto = pd.read_csv('./otrosDatasets/votaciones-diputados.csv')
bloque = pd.read_csv('./otrosDatasets/bloques-diputados.csv')
asuntos = pd.read_csv('./otrosDatasets/asuntos-diputados.csv')

voto_df = pd.DataFrame(data=voto)
diputado_df = pd.DataFrame(data=diputado)
bloque_df = pd.DataFrame(data=bloque)

#inner join: este data frame es voto y diputado mergeado segun id
df = pd.merge(voto_df, bloque_df, left_on='bloqueId', right_on='bloqueId')
df = pd.merge(df,asuntos,left_on = 'asuntoId',right_on = 'asuntoId')

df = df[['bloqueId','bloque','fecha']]
df=df.drop_duplicates()
df["fecha"] = pd.to_datetime(df["fecha"])

timelines= pd.DataFrame([],columns=['bloque', 'fromDate', 'toDate'])
for bloqueId in bloque_df["bloqueId"]:
    fromDate, toDate,bloque=0,0,0
    fromDate=df[df["bloqueId"]==bloqueId]["fecha"].min()
    toDate=df[df["bloqueId"]==bloqueId]["fecha"].max()
    bloque=bloque_df[bloque_df["bloqueId"]==bloqueId].iloc[0]["bloque"]
    timelines.loc[bloqueId]=[bloque,fromDate,toDate]

del diputado,voto,bloque,asuntos,voto_df,diputado_df,bloque_df,df,bloqueId,fromDate,toDate

timelines.to_csv('timelines-bloques.csv')
