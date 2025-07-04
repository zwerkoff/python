import json
import logging
import handlers
from flask import Flask, request, jsonify  # для webhook
from config import TOKEN, SUPPORT
from api import BotHandler
from commands import get_commands

bot = BotHandler(TOKEN)

commands = get_commands()
bot.edit_bot_info(name=None, username=None, description=None, commands=commands, photo=None)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - % (message)s', level=logging.INFO) 
logger = logging.getLogger(__name__)

# res = bot.unsubscribe(url='https://tverregiongaz.ru/f9LHodD0cOJg9ytDU8Cgth6NQxgu2jeO')
# logger.info(f'Статус подписки на webhook:  {res}')


def main():
    while True:
        update = bot.get_updates()  
    
        if update:  
            upd = handlers.update.Update(bot, update)
            if upd.user_id == SUPPORT:
                handlers.support.handler(bot, upd)
            else:
                handlers.client.handler(bot, upd)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()