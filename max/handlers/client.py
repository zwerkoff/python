from api import BotHandler
from FSM import FSM
from handlers.functions import Message, talking_to_support, send_command_support
from commands import text_commands, commands_with_slash
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def handler(bot: BotHandler, msg: Message):
    
    fsm = FSM(bot.storage, msg.user_id)

    if fsm.state:
        
        match fsm.state:
            case 'support':
                id_support = fsm.get_operator_id()
                chat_id_support = fsm.get_operator_chat_id()
                fsm_support = FSM(bot.storage, id_support)
                talking_to_support(bot, msg, fsm, fsm_support, id_support, chat_id_support)
            
            case 'wait_support':
                if msg.text == '/cancel':
                    # при отмене меняем сообщение, которое было отправлено оператору на прошлом шаге. 
                    # ID этого сообщения поместили на прошлом шаге в хранилище абонента
                    id_support = fsm.get_operator_id()
                    fsm_support = FSM(bot.storage, id_support)
                    msg_id = fsm.get_data('zapros')
                    del fsm_support.state
                    del fsm_support.data                    
                    del fsm.state
                    del fsm.data
                    bot.edit_message(msg_id, 'Запрос отменён абонентом', attachments=[])
                    bot.send_message('Запрос отменён.', msg.chat_id, attachments=None)
                else:
                    bot.send_message('Вы в состоянии ожидания диалога с оперетором поддержки. Для отмены отправьте /cancel', msg.chat_id, attachments=None)
        
            case _:
                pass

        return True

    match msg.text:
        case '/help': bot.send_message(text_commands, msg.chat_id, attachments=None)
        case '/support':
            send_command_support(bot, msg)
        case '/count': 
            message_text = 'Здесь будет отрабатывать функция при передаче показаний счётчика'
            bot.send_message(message_text, msg.chat_id, attachments=None)
        case '/info': 
            message_text = f'''Ваш id в max: {msg.user_id}\nВаш name в max: {msg.user_name}\n'''
            bot.send_message(message_text, msg.chat_id, attachments=None)
        case _:
            # Если просто сообщение отправляю список команд бота
            bot.send_message(text_commands, msg.chat_id, attachments=None)

    return True


