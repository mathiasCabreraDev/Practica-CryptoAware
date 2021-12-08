import os
import pandas as pd

RUTA_CSV = '../Historial/data/'
RUTA_IMG = '../Historial/img/'
file = RUTA_CSV+'bitcoin.csv'

if os.path.exists(file):
    df = pd.read_csv(file, index_col=0, parse_dates=True)
    print(df)
    df = df.to_dict('records')
    print(df)


    #TODO
    #Pasar el csv a dict y luego mostrarlo en la pagina 