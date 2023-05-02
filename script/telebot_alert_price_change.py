import telebot
import time
import json
from get_price import get_price

# Load the configuration file
with open('config.json', 'r') as f:
    config = json.load(f)

# Retrieve the Telegram bot token
telegram_bot_token = config['telegram_bot_token']
telegram_chat_id = config['telegram_chat_id']
# Create an instance of the Telegram bot
bot = telebot.TeleBot(telegram_bot_token)

# Define the pairs to monitor and their initial prices
pairs = ['BTCUSDT', 'ETHUSDT']

# Define a function to check the price change for a given pair
def check_price(pair):
    
    price, prev_15min_price, prev_1d_price = get_price(pair)
    perc_change_15min = (price-prev_15min_price)/prev_15min_price * 100
    perc_change_1d = (price-prev_1d_price)/prev_1d_price * 100
    bot.send_message(chat_id=telegram_chat_id, text=f'check price finish, {pair}, {perc_change_15min}')
    # Check if the price change exceeds 1% in the last 5 minutes, 1 hour, or 1 day
    if abs(perc_change_15min) > 0.1 or abs(perc_change_1d) > 0.1:
        # Compose a message to send as an alert
        message = f"{pair} has changed by {perc_change_15min:.2f}% in the last 15 min, {perc_change_1d:.2f}% in the last 1 day. Current price: {price}"

        # Send the message as an alert
        bot.send_message(chat_id=telegram_chat_id, text=message)



# Define a loop to check the price change every 5 minutes
while True:
    # Check the price change for each pair
    for pair in pairs:
        # Check the price change if the pair has an initial price
        check_price(pair)

    # Wait for 5 minutes before checking the price change again
    time.sleep(300)
