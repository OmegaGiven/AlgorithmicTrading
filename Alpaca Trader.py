import alpaca_trade_api as tradeapi


print('''
Stocks to look at :
TMUS, GPRO, BAC, FIT, GE, GERN, IGC, OGEN, ZN, MTNB, NBEV, NEPT, AGRX, DTEA, VTVT, CGC, MSFT
SQ, GRPN, AMD, NVDA, INTC, NTDOY, ATVI, CRON, IIPR, ACB, TSLA
''')
f = open('API.txt', 'r')
if f.mode == 'r':
    file = f.read().split('\n')
f.close()
api = tradeapi.REST(file[0], file[1], file[2])
bought = False


def main():
    while(True):
        customOut = ''
        portfolio = api.list_positions()
        for position in portfolio:
            print("{} shares of {}".format(position.qty, position.symbol))

        symbol = input("\nEnter what Symbol you want to check: ")
        customOut += MACD(symbol) + '\n' + MeanRevision(symbol) + '\n' + MeanRevision21day(symbol)
        print(customOut)
        check = input('do you want to buy or sell? (\'buy\' , \'sell\'):')

        if check == 'buy' and bought(symbol) is False:
            buy(symbol, 50)
        elif check == 'sell' and bought(symbol):
            sell(symbol, 50)
        else:
            continue


def bought(symbol):
    if int(api.get_position(symbol).qty) > 0:
        return True
    else:
        return False


def MACD(symbol):
    out = ''
    barset = api.get_barset(symbol, 'day', limit=5)
    stock = barset[symbol]
    day1 = stock[0].c
    day2 = stock[1].c
    day3 = stock[2].c
    day4 = stock[3].c
    day5 = stock[4].c
    mean = (day1 + day2 + day3 + day4 + day5) / 5
    current = stock[4].o
    if current > mean:
        out += 'Buy ' + symbol + ' at ' + str(current)
    elif current < mean:
        out += 'Sell ' + symbol  + ' at ' + str(current)
    else:
        pass
    return 'MACD Strategy:' + out


def MeanRevision(symbol):
    out = ''
    barset = api.get_barset(symbol, 'day', limit=5)
    stock = barset[symbol]
    day1 = stock[0].c
    day2 = stock[1].c
    day3 = stock[2].c
    day4 = stock[3].c
    day5 = stock[4].c
    mean = (day1 + day2 + day3 + day4 + day5) / 5
    current = stock[4].o
    if current < mean:
        out += 'Buy ' + symbol + ' at ' + str(current)
    elif current > mean:
        out += 'Sell ' + symbol + ' at ' + str(current)
    else:
        pass
    return 'Mean Reversion Strategy: ' + out


def MeanRevision21day(symbol):
    out = ''
    barset = api.get_barset(symbol, 'day', limit=21)
    stock = barset[symbol]
    total = 0
    for x in range(0, 21):
        total += stock[x].c
    mean = total / 21
    current = stock[20].o
    if current < mean * .97:
        out += 'Buy ' + symbol + ' at ' + str(current)
    elif current > mean * 1.03:
        out += 'Sell ' + symbol + ' at ' + str(current)
    else:
        pass
    return 'Mean Reversion 21 day Strategy: ' + out


def buy(symbol, quantity=1):
    f = open('History', 'a+')
    api.submit_order(symbol, quantity, 'buy', 'market', 'gtc')
    f.write('buying: ' + symbol + ' at ' + ' quantity: ' + str(quantity))
    f.close()


def sell(symbol, quantity=1, limit_price=0):
    f = open('History', 'a+')
    if limit_price == 0:
        api.submit_order(symbol, quantity, 'sell', 'limit', 'opg', api.get_position(symbol).current_price)
    else:
        api.submit_order(symbol, quantity, 'sell', 'limit', 'opg', limit_price)
    f.write('\nselling: ' + symbol + ' at ' + ' quantity: ' + str(quantity))


def PrintOrders():
    # Get the last 100 of our closed orders
    closed_orders = api.list_orders(
        status='closed',
        limit=100
    )
    return str(closed_orders)


main()
