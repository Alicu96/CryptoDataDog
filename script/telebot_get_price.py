import ccxt
import telebot
import json

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
    # Create a keyboard with available coin pairs as options
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    for pair in coin_pairs:
        keyboard.add(telebot.types.KeyboardButton(pair))
        
    # Send a message with available coin pairs as options
    response = "Please choose a coin pair:"
    bot.send_message(message.chat.id, response, reply_markup=keyboard)

    # Set the next expected message to be the chosen coin pair
    bot.register_next_step_handler(message, get_price_coin_pair_choice)

# Define the function to process the chosen coin pair
def get_price_coin_pair_choice(message):
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
        
    bot.send_message(message.chat.id, response)

# Start the bot
bot.polling()