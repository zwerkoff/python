from api import BotHandler
from FSM import FSM
from config import SUPPORT
from handlers import support
from commands import text_commands, commands_with_slash



def handler(bot: BotHandler, upd: dict):
    
    user_id = bot.get_user_id(upd)
    fsm = FSM(bot.storage, user_id)
    message_id = bot.get_message_id(upd)
    chat_id = bot.get_chat_id(upd)
    text = bot.get_text(upd)

    # if user_id == SUPPORT:
    #     support.handler(bot, upd)
    #     return True

    if fsm.state:
        pass
        return True

    if text in commands_with_slash:
        match text:
            case '/help': bot.send_message(text_commands, chat_id, attachments=None)
            case '/support': 
                message_text = 'Здесь будет отрабатывать функция при начале разговора с поддержкой'
                bot.send_message(message_text, chat_id, attachments=None)
            case '/count': 
                message_text = 'Здесь будет отрабатывать функция при передаче показаний счётчика'
                bot.send_message(message_text, chat_id, attachments=None)
            case _: 
                name = bot.get_name(upd)
                message_text = f'''Ваш id в max: {user_id}\nВаш name в max: {name}\n'''
                bot.send_message(message_text, chat_id, attachments=None)
        return True


    # Эхо бот. Если просто сообщение отправляю список команд бота
    bot.send_message(text_commands, chat_id, attachments=None)


