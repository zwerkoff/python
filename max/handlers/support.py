from api import BotHandler
from FSM import FSM

def handler(bot: BotHandler, upd: dict):
    
    user_id = bot.get_user_id(upd)
    fsm = FSM(bot.storage, user_id)
    message_id = bot.get_message_id(upd)
    chat_id = bot.get_chat_id(upd)

    if fsm.state:
        pass
        return True

    bot.send_forward_message(None, message_id, chat_id)