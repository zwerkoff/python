import json
import logging
from handlers import client
from flask import Flask, request, jsonify  # для webhook
from config import TOKEN
from api import BotHandler

bot = BotHandler(TOKEN)
commands = [bot.command('id', 'Вывод id пользователя в max'),
            bot.command('help', 'Помощь по основным командам бота'),
            bot.command('ping', 'Игра в пинг понг')]
bot.edit_bot_info(name=None, username=None, description=None, commands=commands, photo=None)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - % (message)s', level=logging.INFO) 
logger = logging.getLogger(__name__)

# res = bot.unsubscribe(url='https://tverregiongaz.ru/f9LHodD0cOJg9ytDU8Cgth6NQxgu2jeO')
# logger.info(f'Статус подписки на webhook:  {res}')


def main():
    while True:
        upd = bot.get_updates()  
    
        if upd:  
           client.handler(bot, upd)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()