import logging
import datetime
import time
from telegram.ext import Updater, CommandHandler
import schedule
from yahoo_trade import *
from coin_news import *

TOKEN = '6228926034:AAG8BP3MllrbJA761HInQmQGd56wZxlOFlU'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

previous_news = ['0']

def start(update, context):
    update.message.reply_text("Hello! I am CrytoBot. I give you news and predict coins for you!!")

def help(update, context):
    update.message.reply_text(
    """
    /start -> Greetings
    /help -> Help
    /content -> Content of the bot
    /contact -> Contact information

    /predict -> It makes a 10-day and 30-day forecast of the cryptocurrency you choose. It gives maximum and minimum estimates. Exp: /predict BTC
    """
    )

def content(update, context):
    update.message.reply_text(
    """
    v0.0
    This bot can send messages of latest news.
    It can forecast next 30 days of a coin.
    It can send forecast data of Ethereium at every night (00:00)
    """
    )


def contact(update, context):
    update.message.reply_text(
    """
    Linkedin: https://www.linkedin.com/in/k%C3%BCr%C5%9Fat-k%C3%B6m%C3%BCrc%C3%BC-303533174/
    Github: https://github.com/kursatkomurcu
    """
    )


def predict(update, context): # Example --> /predict BTC, /predict ETH
    args = context.args  
    if len(args) > 0:
        symbol = args[0] 
        update.message.reply_text(f"Coin: {symbol}")
        update.message.reply_text(f"Please wait. AI is calculating")
        
        forecast30, forecast10, forecast_max, forecast_min, change_percentage30, change_percentage10, change_percentage_max, change_percentage_min = getLSTMResults(symbol)

        update.message.reply_text(f"Price forecasting for after 30 days: {forecast30}")
        update.message.reply_text(f"Change percentage for 30 days: %{change_percentage30}")
        if(change_percentage30 >= 5):
            update.message.reply_text("Buy for 30 days")
        elif(change_percentage30 <= -5):
            update.message.reply_text("Sell for 30 days")
        else:
            update.message.reply_text("Wait for 30 days")

        update.message.reply_text(f"Price forecasting for after 10 days: {forecast10}")
        update.message.reply_text(f"Change percentage for 10 days: %{change_percentage10}")
        if(change_percentage10 >= 5):
            update.message.reply_text("Buy for 10 days")
        elif(change_percentage10 <= -5):
            update.message.reply_text("Sell for 10 days")
        else:
            update.message.reply_text("Wait for 10 days")

        update.message.reply_text(f"Max price forecasting (In 30 days): {forecast_max}")
        update.message.reply_text(f"Change percentage for max price (In 30 days): %{change_percentage_max}")
        if(change_percentage_max >= 5):
            update.message.reply_text("Buy for max price (In 30 days)")
        elif(change_percentage_max <= -5):
            update.message.reply_text("Sell for max price (In 30 days)")
        else:
            update.message.reply_text("Wait for max price (In 30 days)")

        update.message.reply_text(f"Min price forecasting (In 30 days): {forecast_min}")
        update.message.reply_text(f"Change percentage for min price (In 30 days): %{change_percentage_min}")
        if(change_percentage_min >= 5):
            update.message.reply_text("Buy for min price (In 30 days)")
        elif(change_percentage_min <= -5):
            update.message.reply_text("Sell for min price (In 30 days)")
        else:
            update.message.reply_text("Wait for min price (In 30 days)")

    else:
        update.message.reply_text("Please write a crypto currency symbol. Exp: /predict BTC, /predict ETH")

def news():
    data = getNews()
    news_id = data[0]['id']

    if (news_id != previous_news[0]):
        title = data[0]['title']
        body = data[0]['body']
        url = data[0]['url']
            
        date = datetime.utcfromtimestamp(data[0]['published_on'])  
        date = date.strftime('%Y-%m-%d %H:%M:%S')

        message = f"{title}\n\n"
        message += f"{body}\n\n"
        message += f"{url}\n\n"
        message += f"{date}"

        updater.bot.send_message(chat_id=5608974797, text=message)

        previous_news[0] = news_id

            

def job(): # funcion for 00:00 o'clock
    symbol = "ETH"  
    updater.bot.send_message(chat_id=5608974797, text=f"Coin: {symbol}")
    updater.bot.send_message(chat_id=5608974797, text=f"Please wait. AI is calculating")
        
    forecast30, forecast10, forecast_max, forecast_min, change_percentage30, change_percentage10, change_percentage_max, change_percentage_min = getLSTMResults(symbol)

    updater.bot.send_message(chat_id=5608974797, text=f"Price forecasting for after 30 days: {forecast30}")
    updater.bot.send_message(chat_id=5608974797, text=f"Change percentage for 30 days: %{change_percentage30}")
    if(change_percentage30 >= 5):
        updater.bot.send_message(chat_id=5608974797, text="Buy for 30 days")
    elif(change_percentage30 <= -5):
        updater.bot.send_message(chat_id=5608974797, text="Sell for 30 days")
    else:
        updater.bot.send_message(chat_id=5608974797, text="Wait for 30 days")

    updater.bot.send_message(chat_id=5608974797, text=f"Price forecasting for after 10 days: {forecast10}")
    updater.bot.send_message(chat_id=5608974797, text=f"Change percentage for 10 days: %{change_percentage10}")
    if(change_percentage10 >= 5):
        updater.bot.send_message(chat_id=5608974797, text="Buy for 10 days")
    elif(change_percentage10 <= -5):
        updater.bot.send_message(chat_id=5608974797, text="Sell for 10 days")
    else:
        updater.bot.send_message(chat_id=5608974797, text="Wait for 10 days")

    updater.bot.send_message(chat_id=5608974797, text=f"Max price forecasting (In 30 days): {forecast_max}")
    updater.bot.send_message(chat_id=5608974797, text=f"Change percentage for max price (In 30 days): %{change_percentage_max}")
    if(change_percentage_max >= 5):
        updater.bot.send_message(chat_id=5608974797, text="Buy for max price (In 30 days)")
    elif(change_percentage_max <= -5):
        updater.bot.send_message(chat_id=5608974797, text="Sell for max price (In 30 days)")
    else:
        updater.bot.send_message(chat_id=5608974797, text="Wait for max price (In 30 days)")

    updater.bot.send_message(chat_id=5608974797, text=f"Min price forecasting (In 30 days): {forecast_min}")
    updater.bot.send_message(chat_id=5608974797, text=f"Change percentage for min price (In 30 days): %{change_percentage_min}")
    if(change_percentage_min >= 5):
        updater.bot.send_message(chat_id=5608974797, text="Buy for min price (In 30 days)")
    elif(change_percentage_min <= -5):
        updater.bot.send_message(chat_id=5608974797, text="Sell for min price (In 30 days)")
    else:
        updater.bot.send_message(chat_id=5608974797, text="Wait for min price (In 30 days)")

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(CommandHandler("content", content))
dispatcher.add_handler(CommandHandler("contact", contact))
dispatcher.add_handler(CommandHandler("predict", predict))

schedule.every().day.at("00:00").do(job)
schedule.every(1).minutes.do(news)

updater.start_polling()
while True:
    schedule.run_pending()
    time.sleep(1)
