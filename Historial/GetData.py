from os import write
import datetime as dt
import pandas as p
import os.path
from time import sleep

'''Classes import'''
from Modulos import Cryptocurrency

'''API '''
import json
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

'''File'''
FILE = '/home/cryptoaware/cryptoaware.cibermadurez.cl/Historial/data/'


'''
    Consulta la api CoinMarketCap y retorna una lista con diccionario con los precios 
    de las criptomonedas con ids de 1 a 100 por defecto.
    Retorna una lista de diccionarios con la id y el precio

    Retorna: List<dict>
'''
def priceCoinmarketcap(start = '1', limit = '100'):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start': start,
    'limit': limit,
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '',
    }

    session = Session()
    session.headers.update(headers)
    respuestaApi = []
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        for item in data['data']:
            respuestaApi.append({
               item['name'].lower():{
                'name': item['name'].lower(),
                'symbol': item['symbol'],
                'price': item['quote']['USD']['price'],
                'volume': item['quote']['USD']['volume_24h'],
                'market_cap': item['quote']['USD']['market_cap']
                }
            })
        return (respuestaApi)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

def writeCsv(nombre, data):
    archivo = FILE+nombre.replace(' ', '-')+'.csv'
    if os.path.exists(archivo):
        df = p.read_csv(archivo, index_col=[0])
        data = p.DataFrame(data)
        df = df.append(data)
    else:
        df = p.DataFrame(data)
    df.to_csv(archivo)     
    print('File created: {}'.format(archivo))

'''Main'''
crypto = {} # Dict<Cryptocurrency>

primeraConsulta = dt.datetime.now()
print('Los archivos seran generados el {} a las {}.'.format((primeraConsulta + dt.timedelta(days=1)).strftime('%d/%m/%Y'), (primeraConsulta + dt.timedelta(days=1)).strftime('%H:%M:%S')))
#aqui va el ciclo infinito
while(1):
    data = priceCoinmarketcap(limit=100)
    ultimaConsulta = dt.datetime.now()
    print('Consultando... {}'.format(ultimaConsulta.strftime('%H:%M:%S')))
    for d in data:
        key = list(d)[0]
        symbol = d[key]['symbol']
        price = d[key]['price']
        volume = d[key]['volume']
        marketCap = d[key]['market_cap']

        if key in crypto:
            crypto[key].actualizar(price, volume, marketCap)
        else:
            crypto[key] = Cryptocurrency.Cryptocurrency(name=key, symbol=symbol, open=price, volume=volume, marketCap = marketCap)

    if (ultimaConsulta-primeraConsulta)//dt.timedelta(days=1) >= 1:
        for k, v in crypto.items():
            writeCsv(k, v.getData())
            primeraConsulta = dt.datetime.now()
        print('\nLos archivos seran generados el {} a las {}.'.format((primeraConsulta + dt.timedelta(days=1)).strftime('%d/%m/%Y'), (primeraConsulta + dt.timedelta(days=1)).strftime('%H:%M:%S')))
        crypto.clear()
    else:
        print('Esperando... Siguiente consulta a las {}'.format((ultimaConsulta + dt.timedelta(hours=1)).strftime('%H:%M:%S')))
        sleep(60*60) #1 hora de espera
 
