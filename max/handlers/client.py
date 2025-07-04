from api import BotHandler
from FSM import FSM
from config import SUPPORT
from handlers import support
from commands import text_commands, commands_with_slash
import logging
import keyboards

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def command_support(bot: BotHandler, upd):

    chat_id = bot.get_chat_id(upd)
    user_name = bot.get_name(upd)
    user_id = bot.get_user_id(upd)

    # Получаем состояние опретора. 
    # Если не занят отправляем запрос на подключение
    support_state = FSM(bot.storage, SUPPORT)
    
    logger.info(f'state_support: {support_state.state}')
    if support_state.state:
        message_text = 'Оператор в данный момент занят. Попробуйте написать позднее'
        bot.send_message(message_text, chat_id, attachments=None)
        return True
    
    message_text = 'Запрос отправлен оператору. Ожидайте подключения'
    bot.send_message(message_text, chat_id, attachments=None)

    # Добавляю в хранилище данных опретора id абонента
    support_state.data = user_id

    # Отправляю сообщение оператору с клавиатурой
    message_text = f'Абонент: {user_name} ожидает начала диалога'
    keyboard = bot.attach_buttons(keyboards.keyboard_request_support())
    bot.send_message(message_text, chat_id=None, user_id=SUPPORT, attachments=keyboard)

    return True
    
    

def handler(bot: BotHandler, upd: dict):
    
    user_id = bot.get_user_id(upd)
    fsm = FSM(bot.storage, user_id)
    message_id = bot.get_message_id(upd)
    chat_id = bot.get_chat_id(upd)
    text = bot.get_text(upd)

    if user_id == SUPPORT:
        support.handler(bot, upd)
        return True

    if fsm.state:
        if fsm.state == 'support':
            # attach = bot.get_attachments(upd)
            # bot.send_message(text, chat_id=None, user_id=SUPPORT, attachments=attach)

            if text == '/cancel':
                support_state = FSM(bot.storage, SUPPORT)
                del support_state.state
                del support_state.data
                del fsm.state
                bot.send_message('Сеанс завершён.', chat_id=None, user_id=SUPPORT, attachments=None)
                bot.send_message('Сеанс завершён.', chat_id, attachments=None)
            else:
                bot.send_forward_message(text, message_id,chat_id=None, user_id=SUPPORT)
        else:
            pass

        return True

    if text in commands_with_slash:
        match text:
            case '/help': bot.send_message(text_commands, chat_id, attachments=None)
            case '/support':
                command_support(bot, upd)
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


