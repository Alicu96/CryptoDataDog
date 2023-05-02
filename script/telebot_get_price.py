import ccxt
import telebot
import json
from telebot import types

# Define a list of pre-defined coin pairs
coin_pairs = ['BTC/USDT', 'ETH/USDT', 'ADA/USDT']

# Load the configuration file
with open('config.json', 'r') as f:
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
    # Create a message with available coin pairs as options
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(pair) for pair in coin_pairs]
    markup.add(*buttons)
    response = "Please choose a coin pair:"
    
    # Send the message with available coin pairs as buttons
    bot.send_message(message.chat.id, response, reply_markup=markup)

# Define the function to process the chosen coin pair
@bot.message_handler(func=lambda message: True)
def process_coin_pair_choice(message):
    if message.text in coin_pairs:
        try:
            coin_pair = message.text
            
            # Fetch the ticker data for the coin pair
            ticker = exchange.fetch_ticker(coin_pair)
            
            # Extract the price from the ticker data
            price = ticker['last']
            
            # Send the price back to the user
            response = f"Current price of {coin_pair}: {price}"
        except:
            response = "Error: Please choose a valid coin pair from the options."
    else:
        response = "Error: Please choose a valid coin pair from the options."
        
    bot.send_message(message.chat.id, response)

# Start the bot
bot.polling()
