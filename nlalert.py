from telegram.ext import Updater
from auth import telegramToken, ontvangers, havenmeesters, alarmcentrales, personeel

def sendAlert():
    updater = Updater(token=telegramToken)
    dispatcher = updater.dispatcher
    bot = dispatcher.bot
    bericht = "NL-ALERT: De Maeslantkering zal sluiten wegens hoog water."
    berichtPersoneel = "Sluiting in gang gezet, meld u zo snel mogelijk op locatie."
    berichtHavenmeester = "Procedure voor de sluiting van de Maeslantkering is in gang gezet."
    berichtInstanties = "Melding aan instanties: De Measlantkering zal sluiten wegens hoog water"
    for ontvanger in ontvangers:
        bot.sendMessage(chat_id=ontvanger, text=bericht)
    for havenmeester in havenmeesters:
        bot.sendMessage(chat_id=havenmeester, text=berichtHavenmeester)
    for alarmcentrale in alarmcentrales:
        bot.sendMessage(chat_id=alarmcentrale, text=berichtInstanties)
    for persoon in personeel:
        bot.sendMessage(chat_id=persoon, text =berichtPersoneel)
