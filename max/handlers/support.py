from api import BotHandler
from FSM import FSM, MID
from handlers.update import Update
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - % (message)s', level=logging.INFO) 
logger = logging.getLogger(__name__)

def handler(bot: BotHandler, upd: Update):

    fsm = FSM(bot.storage, upd.user_id)

    if fsm.state:
        if fsm.state == 'support':
            abonent_id = fsm.data
            fsm.abonent = FSM(bot.storage, abonent_id)
            mid_storage = MID(bot.storage, abonent_id)

            if upd.text == '/cancel':
                bot.send_message('Сеанс завершён.', chat_id=None, user_id=abonent_id, attachments=None)
                bot.send_message('Сеанс завершён.', upd.chat_id, attachments=None)
                del fsm.abonent.state
                del fsm.state
                del fsm.data
                mid_storage.del_mid()
            else:
                if upd.type_message == 'message_edited':
                    mid_operator = mid_storage.get_value(upd.message_id)
                    bot.edit_message(mid_operator, upd.text)
                elif upd.id_link_message:
                    if upd.link_type == 'reply':
                        mid_abonent = mid_storage.get_value(upd.id_link_message)
                        abonent_chat_id = mid_storage.get_value('abonent_chat_id')
                        send_message = bot.send_reply_message(upd.text, mid_abonent, abonent_chat_id)
                        mid_storage.add_mid(bot.get_message_id(send_message), upd.message_id)
                    else:
                        send_message = bot.send_forward_message(upd.text, upd.message_id, chat_id=None, user_id=abonent_id)
                        mid_storage.add_mid(bot.get_message_id(send_message), upd.message_id)
                else:
                    send_message = bot.send_message(upd.text, chat_id=None, user_id=abonent_id, attachments=upd.attachments)
                    mid_storage.add_mid(bot.get_message_id(send_message), upd.message_id)

        else:
            if upd.text == '/cancel':
                del fsm.state
                bot.send_message('Вы в обычном состоянии', upd.chat_id, attachments=None)
            else:
                bot.send_message('Вы в состоянии "busy"', upd.chat_id, attachments=None)

        return True

    # Ловим нажатие на клавитатуру
    if upd.type_message == 'message_callback':
        if upd.payload == 'start_support':
            bot.edit_message(upd.message_id, 'Начать диалог с абонентом', attachments=[])
            abonent_id = fsm.data
            fsm.abonent = FSM(bot.storage, abonent_id)
            fsm.abonent.state = 'support'
            fsm.state = 'support'
            mid_storage = MID(bot.storage, abonent_id)
            mid_storage.add_operator_chat_id(upd.chat_id)
            bot.send_message('Общение с абонентом началось.\n Для завершения разговора отправьте команду /cancel', upd.chat_id, attachments=None)
            bot.send_message(f'Общение с оператором началось.\n Для завершения разговора отправьте команду /cancel', chat_id=None, user_id=abonent_id, attachments=None)
        
        return True

    if upd.text == '/busy':
        fsm.state = 'busy'
        bot.send_message('Вы перешли в состоянии "busy"', upd.chat_id, attachments=None)
        return True
        

    bot.send_message(f'/busy - перейти в состояние "busy".\n/cancel - вернуться в обычное состояние', upd.chat_id, attachments=None)
    # logger.info(upd)

    return True