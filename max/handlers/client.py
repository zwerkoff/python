from api import BotHandler
from FSM import FSM, MID
from handlers.update import Update
from config import SUPPORT
from commands import text_commands, commands_with_slash
import logging
import keyboards

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def command_support(bot: BotHandler, upd: Update):

    # Получаем состояние опретора. 
    # Если не занят отправляем запрос на подключение
    fsm_support = FSM(bot.storage, SUPPORT)
    fsm = FSM(bot.storage, upd.user_id)
    
    if fsm_support.state:
        bot.send_message('Оператор в данный момент занят. Попробуйте написать позднее', upd.chat_id, attachments=None)
    else:    
        bot.send_message('Запрос отправлен оператору. Ожидайте подключения', upd.chat_id, attachments=None)

        # Добавляю в хранилище данных опретора id абонента
        # Меняю состояние абонента на 'wait_support'
        fsm_support.data = upd.user_id
        fsm.state = 'wait_support'
        
        # Отправляю сообщение оператору с клавиатурой
        message_text = f'Абонент: {upd.user_name} ожидает начала диалога'
        message = bot.send_message(message_text, chat_id=None, user_id=SUPPORT, attachments=keyboards.request_support())
        
        # Получаю идентификатор отправленного сообщения. Записываю его в хранилище абонента
        # Если абонент передумает на следующем шаге, изменю это сообшение
        mid = bot.get_message_id(message)
        fsm.data = mid

        mid_storage = MID(bot.storage, upd.user_id)
        mid_storage.add_abonent_chat_id(upd.chat_id)
    
    return True    
    

def handler(bot: BotHandler, upd: Update):
    
    fsm = FSM(bot.storage, upd.user_id)

    if fsm.state:

        mid_storage = MID(bot.storage, upd.user_id)

        if fsm.state == 'support':

            if upd.text == '/cancel':
                # при отмене сбрасывает состояния оператора и абонента
                fsm_support = FSM(bot.storage, SUPPORT)

                bot.send_message('Сеанс завершён.', chat_id=None, user_id=SUPPORT, attachments=None)
                bot.send_message('Сеанс завершён.', upd.chat_id, attachments=None)

                del fsm_support.state
                del fsm_support.data
                del fsm.state
                mid_storage.del_mid()
            else:
                if upd.type_message == 'message_edited':
                    mid_operator = mid_storage.get_value(upd.message_id)
                    bot.edit_message(mid_operator, upd.text)
                elif upd.id_link_message:
                    if upd.link_type == 'reply':
                        mid_operator = mid_storage.get_value(upd.id_link_message)
                        operator_chat_id = mid_storage.get_value('operator_chat_id')
                        send_message = bot.send_reply_message(upd.text, mid_operator, operator_chat_id)
                        mid_storage.add_mid(bot.get_message_id(send_message), upd.message_id)
                    else:
                        send_message = bot.send_forward_message(upd.text, upd.message_id, chat_id=None, user_id=SUPPORT)
                        mid_storage.add_mid(bot.get_message_id(send_message), upd.message_id)

                else:
                    send_message = bot.send_message(upd.text, chat_id=None, user_id=SUPPORT, attachments=upd.attachments)
                    mid_storage.add_mid(bot.get_message_id(send_message), upd.message_id)
        
        elif fsm.state == 'wait_support':
            if upd.text == '/cancel':
                # при отмене меняем сообщение, которое было отправлено оператору на прошлом шаге. 
                # ID этого сообщения поместили на прошлом шаге в хранилище абонента
                mid = fsm.data
                bot.edit_message(mid, 'Запрос отменён абонентом', attachments=[])
                del fsm.state
                del fsm.data
                mid_storage.del_mid()
                bot.send_message('Запрос отменён.', upd.chat_id, attachments=None)
            else:
                bot.send_message('Вы в состоянии ожидания диалога с оперетором поддержки. Для отмены отправьте /cancel', upd.chat_id, attachments=None)
        
        else:
            pass

        return True



    match upd.text:
        case '/help': bot.send_message(text_commands, upd.chat_id, attachments=None)
        case '/support':
            command_support(bot, upd)
        case '/count': 
            message_text = 'Здесь будет отрабатывать функция при передаче показаний счётчика'
            bot.send_message(message_text, upd.chat_id, attachments=None)
        case '/info': 
            message_text = f'''Ваш id в max: {upd.user_id}\nВаш name в max: {upd.user_name}\n'''
            bot.send_message(message_text, upd.chat_id, attachments=None)
        case _:
            # Если просто сообщение отправляю список команд бота
            bot.send_message(text_commands, upd.chat_id, attachments=None)

    return True


