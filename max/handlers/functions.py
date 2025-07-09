from api import BotHandler
from FSM import FSM
from config import SUPPORT
import logging
import keyboards


class Message:
    """
    Класс для удобной работы с данными сообщения

    :param 
        bot - экземляр класса BotHandler
        message - данные полученные при помощи метода get_update класса bot
    """

    def __init__(self, bot: BotHandler, message: dict):
        self.bot = bot
        self.message = message
    
    @property
    def chat_id(self):
        """
        Возвращает id чата пользователя с ботом
        """
        return self.bot.get_chat_id(self.message)

    @property
    def user_id(self):
        """
        Возвращает id пользователя отправившего сообщение
        """
        return self.bot.get_user_id(self.message)
    
    @property
    def user_name(self):
        """
        Возвращает имя пользователя в Max
        """
        return self.bot.get_name(self.message)

    @property
    def message_id(self):
        """
        Возвращает id сообщения
        """
        return self.bot.get_message_id(self.message)

    @property
    def text(self):
        """
        Возвращает текст сообщения
        """
        return self.bot.get_text(self.message)

    @property
    def attachments(self):
        """
        Возвращает все вложения сообщения
        """
        return self.bot.get_attachments(self.message)

    @property
    def payload(self):
        """
        Возвращает значение нажатой кнопки
        """
        return self.bot.get_payload(self.message)

    @property
    def type_message(self):
        """
        Возвращает тип сообщения. Например: message_callback, message_edited

        https://dev.max.ru/docs-api/objects/Update
        """
        return self.bot.get_update_type(self.message)

    @property
    def id_link_message(self):
        """
        Получение message_id пересланного сообщения
        """
        link_message = self.bot.get_link_message(self.message)
        if link_message:
            return link_message.get('mid')
        return None

    @property
    def link_type(self):
        """
        Получение типа пересланного сообщения

        reply или forward
        """
        return self.bot.get_link_type(self.message)

def get_support(bot: BotHandler):
    """
    возвращает id первого свободного оператора поддержки
    """
    for id in SUPPORT:
        fsm_support = FSM(bot.storage, id)
        if not fsm_support.state:
            return id
    return None


def send_command_support(bot: BotHandler, msg: Message):
    """
    Действие при отправке команды /support
    """

    support_id = get_support(bot)
    if support_id is None:
        bot.send_message('Все операторы поддержки в данный момент заняты. Попробуйте написать позднее', msg.chat_id)
    else:    
        fsm = FSM(bot.storage, msg.user_id)
        fsm.state = 'wait_support'
        fsm.add_abonent_info(msg.chat_id, msg.user_id)
        fsm.add_operator_info(None, support_id)

        fsm_support = FSM(bot.storage, support_id)
        fsm_support.state = 'wait_support'
        fsm_support.data = msg.user_id
        
        bot.send_message('Запрос отправлен оператору. Ожидайте подключения', msg.chat_id)

        # Отправляю сообщение оператору с клавиатурой
        message_text = f'Абонент: {msg.user_name}\nid: {msg.user_id}\nожидает начала диалога'
        message = bot.send_message(message_text, chat_id=None, user_id=support_id, attachments=keyboards.request_support())
        
        # Получаю идентификатор отправленного сообщения. Записываю его в хранилище абонента
        # Если абонент передумает на следующем шаге, изменю это сообшение
        fsm.add_key_and_value('zapros', bot.get_message_id(message))
    
    return True    

def talking_to_support(bot: BotHandler, msg: Message, fsm_abonent: FSM, fsm_support: FSM, id_other_side: int, chat_id_other_side: int):
    """
    Действия оператора и абонента в статусе support

    id_other_side - id собеседника. Для оператора указать id абонента. Для абоненте указать id оператора
    chat_id_other_side - id чата собеседника с ботом. 
    """
    
    if msg.text == '/cancel':
        # при отправке команды /cancel удаляем состояние и данные оператора и абонента
        del fsm_abonent.state
        del fsm_abonent.data
        del fsm_support.state
        del fsm_support.data
        bot.send_message('Сеанс завершён.', chat_id=None, user_id=id_other_side)
        bot.send_message('Сеанс завершён.', msg.chat_id)

    else:

        # если сообщение изменено. Ищем id такого же сообщения у собеседника и тоже меняем
        if msg.type_message == 'message_edited':
            msg_id = fsm_abonent.get_data(msg.message_id)
            bot.edit_message(msg_id, msg.text)

        elif msg.type_message == 'message_removed':
            msg_id = fsm_abonent.get_data(msg.message_id)
            bot.delete_message(msg_id)

        # если у сообщения есть link, значит оно как ответ(reply) или пересылаемое(forward)
        # после отправки записываем id сообщения в data абонента
        elif msg.id_link_message:

            if msg.link_type == 'reply':
                msg_id = fsm_abonent.get_data(msg.id_link_message)
                message = bot.send_reply_message(msg.text, msg_id, chat_id_other_side)
                fsm_abonent.add_mid(bot.get_message_id(message), msg.message_id)
            
            else:
                message = bot.send_forward_message(msg.text, msg.message_id, chat_id=None, user_id=id_other_side)
                fsm_abonent.add_mid(bot.get_message_id(message), msg.message_id)
        
        # Иначе если обычное сообщение, пересылаем его собеседнику через бота.
        # после отправки записываем id сообщения в data абонента
        else:
            message = bot.send_message(msg.text, chat_id=None, user_id=id_other_side, attachments=msg.attachments)
            fsm_abonent.add_mid(bot.get_message_id(message), msg.message_id)
