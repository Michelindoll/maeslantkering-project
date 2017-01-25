from telegram.ext import Updater
from auth import telegramToken, ontvangers

def sendAlert():
    updater = Updater(token=telegramToken)
    dispatcher = updater.dispatcher
    bot = dispatcher.bot
    bericht = "NL-ALERT: De Maeslantkering zal sluiten wegens hoog water."
    for ontvanger in ontvangers:
        bot.sendMessage(chat_id=ontvanger, text=bericht)
