import json
import logging
import client
from flask import Flask, request, jsonify  # для webhook
from config import TOKEN
from api import BotHandler

bot = BotHandler(TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - % (message)s', level=logging.INFO) 
logger = logging.getLogger(__name__)

commands = [bot.command('id', 'Вывод id пользователя в max'),
            bot.command('help', 'Помощь по основным командам бота'),
            bot.command('ping', 'Игра в пинг понг')]
bot.edit_bot_info(name=None, username=None, description=None, commands=commands, photo=None)
subscribe = bot.subscribe(url='https://tverregiongaz.ru/f9LHodD0cOJg9ytDU8Cgth6NQxgu2jeO')
logger.info(f'Статус подписки на webhook:  {subscribe}')

# для подписки на webhook через @masterbot и команду /set_webhook 
# задать адрес и порт (см. конец кода) сервера где размещен бот 
# например: http://123.123.123.123:33333 или http://myserver.com:17235 
# допустимые порты 80, 8080, 443, 8443, 16384-32383 
# это простой, но не безопасный способ, представлен для понимания работы

app = Flask(__name__)  # для webhook


@app.route('/', methods=['POST'])  # для webhook 
def main():
   
    while True:
        upd = request.get_json()  
        # получаем внутреннее представление сообщения (контента) отправленного боту (сформированного ботом)
        # этот способ не формирует событие (mark_seen) о прочтении ботом сообщения, нужно формировать его самостоятельно 
        
        if upd:  
            client.register_handlers(bot, upd)    
            
        return jsonify(upd)  # для webhook


if __name__ == '__main__':  # для webhook
    try:
        app.run(port=3002, host="0.0.0.0") # порт нужно выбирать нестандартный для уменьшения количества атак
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