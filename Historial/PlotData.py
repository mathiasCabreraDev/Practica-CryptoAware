from os import path
import pandas as pd
import os
import datetime
import plotly.graph_objects as go

FILE = './data/'
GRAPHS = './graphs/'

'''
    parametros:
        name: [string] nombre del archivo ubicado en ./data/

    grafica los datos y lois
'''
def graficar(name):
    files = os.listdir(FILE)
    if name in files:
        if name[-4:] == '.csv':
            dirName = name[:-4] #para crear directorio
            graphDir = GRAPHS+dirName+'/'
            fileName = graphDir+name[:-4]+'.html'

            if dirName not in os.listdir(GRAPHS):
                os.makedirs(graphDir)

            dataFromFile = pd.read_csv(FILE+name, index_col=0, parse_dates=True)
            dates = list()
            for f in  dataFromFile.date.to_list():
                d =  f.split('-')
                dates.append(datetime.date(day= int(d[0]), month= int(d[1]), year= int(d[2])))
            fig = go.Figure(
                data=[go.Candlestick(
                    x=dates,
                    open=dataFromFile.open.to_list(),
                    high=dataFromFile.high.to_list(),
                    low=dataFromFile.low.to_list(),
                    close=dataFromFile.close.to_list(),
                )]
            )
            fig.update_layout(
                title= '{} ({})'.format(name[:-4].capitalize(), dataFromFile.symbol.to_list()[0])
            )
            
            fig.write_html(fileName)
