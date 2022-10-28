
"""
Simple Bot to reply to Telegram messages taken from the python-telegram-bot examples.
Source: https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot2.py
"""

import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Ativando os logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
PORT = int(os.environ.get('PORT', 8443))
TOKEN = os.environ['TOKEN']

# Defina alguns manipuladores de comandos. Estes geralmente levam a atualização de dois argumentos e
# contexto. Os manipuladores de erro também recebem o objeto TelegramError gerado com erro.

def hello(update, context):
    # Responde quando o comando /hello é enviado
    update.message.reply_text('Hey!\nNosso servidor está ligado, eu estou vivo 🫡')

def help(update, context):
    # Responde quando o comando /help é enviado
    update.message.reply_text('Help!')

def echo(update, context):
    # Repete a mensagem enviada pelo usuario
    update.message.reply_text(update.message.text)

def error(update, context):
    #Erros de log causados ​​por atualizações.
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("hello", hello))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url='https://telebot-py.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()