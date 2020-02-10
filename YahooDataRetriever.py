import datetime
from pandas import pandas_datareader as pdr


def get_data(symbol, start = datetime.datetime(2018, 1, 1), end = datetime.datetime(2019, 12, 31)):
    return pdr.get_data_yahoo(symbol, start=start, end=end)


def main():
    symbol = input('Type symbol of company for financial data:')
    yearStart = int(input('from the beginning of what year:'))
    yearEnd = int(input('to the end of what year:'))
    data =  get_data(symbol, yearStart, yearEnd)
    print(data)
    f = open(symbol + data + '.csv', 'w+')
    f.write(data)
    f.close()


main()
