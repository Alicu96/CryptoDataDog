import ccxt
import telebot
import json
import sys

file_config = sys.argv[1]

# Load the configuration file
with open(file_config, 'r') as f:
    config = json.load(f)

# Retrieve the Telegram bot token
telegram_bot_token = config['telegram_bot_token']

# Create an instance of the Telegram bot
bot = telebot.TeleBot(telegram_bot_token)

# Create an instance of the exchange (in this case Binance)
exchange = ccxt.binance()

# Define the function to handle the '/price' command
@bot.message_handler(commands=['price'])
def send_price(message):
    try:
        # Extract the coin pair from the message text
        coin_pair = message.text.split()[1].upper()
        
        # Fetch the ticker data for the coin pair
        ticker = exchange.fetch_ticker(coin_pair)
        
        # Extract the price from the ticker data
        price = ticker['last']
        
        # Send the price back to the user
        response = f"Current price of {coin_pair}: {price}"
    except:
        response = "Error: Please enter a valid coin pair (e.g. BTC/USDT)"
        
    bot.send_message(message.chat.id, response)

# Start the bot
bot.polling()