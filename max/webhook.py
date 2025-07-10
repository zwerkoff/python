import json
import logging
import client
import handlers
from flask import Flask, request, jsonify  # для webhook
from config import *
from api import BotHandler
from commands import get_commands


bot = BotHandler(TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - % (message)s', level=logging.INFO) 
logger = logging.getLogger(__name__)

# Если подписка на webhook не установлена - устанавливаем
if not bot.get_subscriptions():
    subscribe = bot.subscribe(url=WEBHOOK)

commands = get_commands()
bot.edit_bot_info(name=None, username=None, description=None, commands=commands, photo=None)

# для подписки на webhook через @masterbot и команду /set_webhook 
# задать адрес и порт (см. конец кода) сервера где размещен бот 
# например: http://123.123.123.123:33333 или http://myserver.com:17235 или 
# допустимые порты 80, 8080, 443, 8443, 16384-32383 
# это простой, но не безопасный способ, представлен для понимания работы
# мой способ: webhook такого плана https://myserver.com/anypath 
# На сервере конфигурируем Apache: в файле myserver.conf добавляю строку ProxyPass /anypath http://localhost:port

app = Flask(__name__)
@app.route('/', methods=['POST'])
def main():
   
    while True:
        update = request.get_json()  
        # получаем внутреннее представление сообщения (контента) отправленного боту (сформированного ботом)
        # этот способ не формирует событие (mark_seen) о прочтении ботом сообщения, нужно формировать его самостоятельно 
        bot.mark_seen(update)
        
        if update:  
            msg = handlers.functions.Message(bot, update)
            if msg.user_id in SUPPORT:
                handlers.support.handler(bot, msg)
            else:
                handlers.client.handler(bot, msg)  
            
        return jsonify(upd)  

if __name__ == '__main__':  
    try:
        app.run(port=PORT, host="0.0.0.0") 
    except KeyboardInterrupt:
        exit()











# def main():
#   while True:
#     upd = bot.get_updates()  # получаем внутреннее представление сообщения (контента) отправленного боту (сформированного ботом)
#     # тут можно вставить любые действия которые должны выполняться во время ожидания события
#     if upd:  # основной код, для примера представлен эхо-бот
#       chat_id = bot.get_chat_id(upd)
#       text = bot.get_text(upd)
#       bot.send_message(text, chat_id)


# if __name__ == '__main__':
#   try:
#     main()
#   except KeyboardInterrupt:
#     exit()