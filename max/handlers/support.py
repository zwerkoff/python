from api import BotHandler
from FSM import FSM

def handler(bot: BotHandler, upd: dict):
    
    user_id = bot.get_user_id(upd)
    fsm = FSM(bot.storage, user_id)
    message_id = bot.get_message_id(upd)
    chat_id = bot.get_chat_id(upd)
    type_message = bot.get_update_type(upd)
    text = bot.get_text(upd)

    if fsm.state:
        if fsm.state == 'support':
            
            abonent_id = fsm.data
            abonent_state = FSM(bot.storage, abonent_id)

            if text == '/cancel':
                del abonent_state.state
                del fsm.state
                del fsm.data
                bot.send_message('Сеанс завершён.', chat_id=None, user_id=abonent_id, attachments=None)
                bot.send_message('Сеанс завершён.', chat_id, attachments=None)
            else:
                attach = bot.get_attachments(upd)
                bot.send_message(text, chat_id=None, user_id=abonent_id, attachments=attach)

        else:
            message_text = 'Вы в состоянии "busy"'
            bot.send_message(message_text, chat_id, attachments=None)

        return True

    # Ловим нажатие на клавитатуру
    if type_message == 'message_callback':
        callback_id = bot.get_callback_id(upd)
        payload = bot.get_payload(upd)
        if payload == 'start_support':
            bot.edit_message(message_id, 'Начать диалог с абонентом', attachments=[])
            abonent_id = fsm.data
            abonent_state = FSM(bot.storage, abonent_id)
            abonent_state.state = 'support'
            fsm.state = 'support'
            bot.send_message('Общение с абонентом началось.\n Для завершения разговора отправьте команду /cancel', chat_id, attachments=None)
            bot.send_message(f'Общение с оператором началось.\n Для завершения разговора отправьте команду /cancel', chat_id=None, user_id=abonent_id, attachments=None)
        
        return True

    if text == '/busy':
        fsm.state = 'busy'
        message_text = 'Вы перешли в состоянии "busy"'
        bot.send_message(message_text, chat_id, attachments=None)
        return True
        

    # bot.send_forward_message(None, message_id, chat_id)

    return True