from telegram.ext import Updater
from auth import telegramToken, ontvangers, havenmeesters, alarmcentrales

def sendAlert():
    updater = Updater(token=telegramToken)
    dispatcher = updater.dispatcher
    bot = dispatcher.bot
    bericht = "NL-ALERT: De Maeslantkering zal sluiten wegens hoog water."
    berichtHavenmeester = "Procedure voor de sluiting van de Maeslantkering is in gang gezet."
    for ontvanger in ontvangers:
        bot.sendMessage(chat_id=ontvanger, text=bericht)
    for havenmeester in havenmeesters:
        bot.sendMessage(chat_id=havenmeester, text=bericht)
    for alarmcentrale in alarmcentrales:
        bot.sendMessage(chat_id=alarmcentrales, text=bericht)
