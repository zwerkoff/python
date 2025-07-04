from api import BotHandler
from FSM import FSM
from handlers.update import Update

def handler(bot: BotHandler, upd: Update):

    fsm = FSM(bot.storage, upd.user_id)

    if fsm.state:
        if fsm.state == 'support':
            abonent_id = fsm.data
            fsm.abonent = FSM(bot.storage, abonent_id)

            if upd.text == '/cancel':
                del fsm.abonent.state
                del fsm.state
                del fsm.data
                bot.send_message('Сеанс завершён.', chat_id=None, user_id=abonent_id, attachments=None)
                bot.send_message('Сеанс завершён.', upd.chat_id, attachments=None)
            else:
                bot.send_message(upd.text, chat_id=None, user_id=abonent_id, attachments=upd.attachments)

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
            bot.send_message('Общение с абонентом началось.\n Для завершения разговора отправьте команду /cancel', upd.chat_id, attachments=None)
            bot.send_message(f'Общение с оператором началось.\n Для завершения разговора отправьте команду /cancel', chat_id=None, user_id=abonent_id, attachments=None)
        
        return True

    if upd.text == '/busy':
        fsm.state = 'busy'
        bot.send_message('Вы перешли в состоянии "busy"', upd.chat_id, attachments=None)
        return True
        

    bot.send_message(f'/busy - перейти в состояние "busy".\n/cancel - вернуться в обычное состояние', upd.chat_id, attachments=None)

    return True