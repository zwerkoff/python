import json
import logging
import handlers
import os
from config import TOKEN, SUPPORT, WEBHOOK
from api import BotHandler
from commands import get_commands

bot = BotHandler(TOKEN)

commands = get_commands()
bot.edit_bot_info(name=None, username=None, description=None, commands=commands, photo=None)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - % (message)s', level=logging.INFO) 
logger = logging.getLogger(__name__)

# Если подписка на webhook установлена - убираем
if bot.get_subscriptions():
    res = bot.unsubscribe(url=WEBHOOK)

def main():
    while True:
        update = bot.get_updates()  
    
        if update:  
            msg = handlers.functions.Message(bot, update)
            if msg.user_id in SUPPORT:
                handlers.support.handler(bot, msg)
            else:
                handlers.client.handler(bot, msg)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()