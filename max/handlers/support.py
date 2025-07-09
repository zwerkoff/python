from api import BotHandler
from FSM import FSM
from handlers.functions import Message, talking_to_support
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - % (message)s', level=logging.INFO) 
logger = logging.getLogger(__name__)

def handler(bot: BotHandler, msg: Message):

    fsm = FSM(bot.storage, msg.user_id)

    
    # Ловим нажатие на клавитатуру
    if msg.type_message == 'message_callback':
        
        if msg.payload == 'start_support':
            # меняем состояние оператора и абонента
            id_abonent = fsm.data
            fsm_abonent = FSM(bot.storage, id_abonent)
            fsm_abonent.state = 'support'
            fsm_abonent.add_operator_info(msg.chat_id, msg.user_id)
            fsm.state = 'support'
            
            bot.edit_message(msg.message_id, 'Начать диалог с абонентом', attachments=[])
            bot.send_message(f'Общение с абонентом началось.\n Для завершения разговора отправьте команду /cancel', msg.chat_id, attachments=None)
            bot.send_message(f'Общение с оператором началось.\n Для завершения разговора отправьте команду /cancel', chat_id=None, user_id=id_abonent, attachments=None)
        
        return True

    if fsm.state:

        match fsm.state:
            case 'support':
                id_abonent = fsm.data
                fsm_abonent = FSM(bot.storage, id_abonent)
                talking_to_support(bot, msg, fsm_abonent, fsm, id_abonent, fsm_abonent.get_abonent_chat_id())
            
            case 'wait_support':
                bot.send_message('Вы в состоянии "wait_support". Ответьте абоненту', msg.chat_id)

            case _:
                if msg.text == '/cancel':
                    del fsm.state
                    bot.send_message('Вы в обычном состоянии', msg.chat_id)
                else:
                    bot.send_message('Вы в состоянии "busy"', msg.chat_id)

        return True


    if msg.text == '/busy':
        fsm.state = 'busy'
        bot.send_message('Вы перешли в состоянии "busy"', msg.chat_id, attachments=None)
        return True

    bot.send_message(f'/busy - перейти в состояние "busy".\n/cancel - вернуться в обычное состояние', msg.chat_id, attachments=None)

    return True