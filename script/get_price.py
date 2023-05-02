import ccxt
import time

exchange = ccxt.coinbasepro()

def get_price(coin_name, coin_ref='USD'):
    pair = f'{coin_name}/{coin_ref}'
    ticker = exchange.fetch_ticker(pair)
    price = ticker['last']
    return price

if __name__=='__main__':
    import sys
    coin_name = sys.argv[1]
    price = get_price(coin_name=coin_name)
    print(price)


