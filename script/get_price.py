import ccxt
import time

exchange = ccxt.coinbasepro()

while True:
    ticker = exchange.fetch_ticker('BTC/USD')
    price = ticker['last']
    print(f"BTC price: ${price}")
    time.sleep(300) # wait for 5 minutes
