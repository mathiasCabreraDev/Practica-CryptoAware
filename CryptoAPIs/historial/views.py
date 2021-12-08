from django import template
import historial
from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import Http404
from django.template import loader

from requests import Session
from requests import api
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import datetime as dt
import os
import pandas as pd

import datetime
import plotly.graph_objects as go
#RUTAS
RUTA_CSV = '/home/cryptoaware/cryptoaware.cibermadurez.cl/Historial/data/'
RUTA_GPH = '/home/cryptoaware/cryptoaware.cibermadurez.cl/Historial/graphs/'
TEMPLATES_GRAPHS = '/home/cryptoaware/cryptoaware.cibermadurez.cl/CryptoAPIs/historial/templates/historial/graphs/' 

'''
    name: String con la forma de un archivo .csv
    Genera los graficos de la data solicitada
'''
def generarGrafico(name):
    files = os.listdir(RUTA_CSV)
    if name in files:
        if name[-4:] == '.csv':
            dirName = name[:-4] #para crear directorio
            graphDir = RUTA_GPH+dirName+'/'
            fileName =TEMPLATES_GRAPHS+name[:-4]+'.html'

            if dirName not in os.listdir(RUTA_GPH):
                os.makedirs(graphDir)

            dataFromFile = pd.read_csv(RUTA_CSV+name, index_col=0, parse_dates=True)
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

def grafico(request, id):
    file = id.replace('%2520','-')+'.csv'
    generarGrafico(file)
    name = id.replace(' ','-')+'.html'
    template = loader.get_template('historial/grafico.html')
    context = {
        'name': id,
        'graph': name
    }
    return HttpResponse(template.render(context, request))
    	
def cryptocoin(request, id):
    df = ''
    name = id.replace('%2520',' ').title()
    symbol = ''

    file = RUTA_CSV+id.replace('%2520','-')+'.csv'
    if os.path.exists(file):
        df = pd.read_csv(file, index_col=0, parse_dates=True)
        df = df.to_dict('records')
    else:
        raise Http404("Lo que buscabas no existe. :(")

    symbol = df[0]['symbol']

    template = loader.get_template('historial/cryptocoin.html')  
    context = {
        'data': df,
        'name': name,
        'symbol': symbol,
        'file': id.replace('%2520', '-')
    }
    return HttpResponse(template.render(context, request))

def index(request):
    monedas = [i[:-4].replace('-',' ') for i in os.listdir(RUTA_CSV)]
    
    template = loader.get_template('historial/index.html')
    context = {
        'data': monedas,     
    }
    return HttpResponse(template.render(context, request))
