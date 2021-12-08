import datetime as dt

class Cryptocurrency:
    def __init__(self, name, symbol, open, volume, marketCap):
        self.__name = name
        self.__symbol = symbol
        self.__open = open
        self.__high = open
        self.__low = open
        self.__close = open
        self.__volume = volume
        self.__marketCap = marketCap

    def actualizar(self, price, volumen, marketCap):
        self.__high = price if self.__high < price else self.__high
        self.__low = price if self.__low > price else self.__low
        self.__close = price
        self.__volume = volumen
        self.__marketCap = marketCap

    def getData(self):
        return [{
            'date': dt.datetime.now().strftime('%d-%m-%Y'),
            'symbol': self.__symbol,
            'open': self.__open,
            'high': self.__high,
            'low': self.__low,
            'close': self.__close,
            'volume': self.__volume,
            'market_cap': self.__marketCap
        }]