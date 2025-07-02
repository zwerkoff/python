from api import BotHandler
import FSM
import keyboards
from time import sleep

def handler(bot: BotHandler, upd: dict):
    chat_id = bot.get_chat_id(upd)
    text = bot.get_text(upd)
    message_id = bot.get_message_id(upd)
    user_id = bot.get_user_id(upd)
    type_message = bot.get_update_type(upd)
    commands = bot.get_bot_commands()
    commands = [f"/{i['name']}" for i in commands]

    # Ловим нажатие на клавитатуру
    if type_message == 'message_callback':
        callback_id = bot.get_callback_id(upd)
        payload = bot.get_payload(upd)
        
        match payload:
            case '1': bot.send_message(f'вы нажали {payload}', chat_id)
            case '2': bot.send_answer_callback(callback_id, None, f'вы нажали {payload}')
            case '3': bot.edit_message(message_id, 'Нажатие на кнопку 3')
            case _:
                # bot.send_answer_callback(callback_id, notification=None, text=f'вы нажали {payload}',attachments=None)
                # bot.send_message(f'вы нажали {payload}', chat_id)
                bot.delete_message(message_id)
                sleep(0.2)
                bot.send_message(f'вы нажали {payload}', chat_id)
        return True

    # Ловим команды
    if text in commands:
        match text:
            case '/id': bot.send_message(f'Ваш id в max: {user_id}', chat_id)
            case '/help': bot.send_message(f'Доступные команды бота: {bot.get_bot_commands()}', chat_id)
            case '/ping': 
                key = keyboards.test(bot)
                bot.send_buttons('None', key, chat_id)
                # FSM.state(chat_id, 'start')
                # bot.send_reply_message(f'pong: {FSM.get_state(chat_id)}', message_id , chat_id)
                # FSM.state(chat_id, 'finish')
                # bot.send_reply_message(f'pong: {FSM.get_state(chat_id)}', message_id , chat_id)
                # FSM.finish(chat_id)
                # bot.send_reply_message(f'pong: {FSM.get_state(chat_id)}', message_id , chat_id)
            case _: bot.send_message(text, chat_id)
        return True

    # Просто отвечаем на сообщение
    bot.send_message(text, chat_id)
    return True


    





# class Handler():

#     def __init__(self, bot: BotHandler):
#         self.bot = bot
#         self.upd = self.bot.get_updates()
#         self.chat_id = self.bot.get_chat_id(self.upd)
#         self.text = self.bot.get_text(self.upd)

#     def message(self):
#         text = f'Пересылаю текст: {self.text}'
#         self.bot.send_message(text, self.chat_id)

#     def command(self):
#         text = f'Пересылаю команду: {self.text}'
#         self.bot.send_message(text, self.chat_id)



# def register_handlers(bot: BotHandler, upd):
    
#     chat_id = bot.get_chat_id(upd)
#     bot.mark_seen(chat_id)
#     text = bot.get_text(upd)
#     message_id = bot.get_message_id(upd)
#     user_id = bot.get_user_id(upd)
#     type_message = bot.get_update_type(upd)

#     if type_message == 'message_callback':
#         callback_id = bot.get_callback_id(upd)
#         payload = bot.get_payload(upd)
        
#         match payload:
#             case '1': bot.send_message(f'вы нажали {payload}', chat_id)
#             case '2': bot.send_answer_callback(callback_id, None, f'вы нажали {payload}')
#             case '3': 
#                 bot.edit_message(message_id, 'test well ...')
#             case _:
#                 bot.send_answer_callback(callback_id, notification=None, text=f'вы нажали {payload}',attachments=None)
#                 bot.send_message(f'вы нажали {payload}', chat_id)
#                 bot.delete_message(message_id)

#     match text:
#         case '/id': bot.send_message(f'Ваш id в max: {user_id}', chat_id)
#         case '/help': bot.send_message(f'Доступные команды бота: {bot.get_bot_commands()}', chat_id)
#         case '/ping': 
#             key = keyboards.test(bot)
#             bot.send_buttons('None', key, chat_id)
#             # FSM.state(chat_id, 'start')
#             # bot.send_reply_message(f'pong: {FSM.get_state(chat_id)}', message_id , chat_id)
#             # FSM.state(chat_id, 'finish')
#             # bot.send_reply_message(f'pong: {FSM.get_state(chat_id)}', message_id , chat_id)
#             # FSM.finish(chat_id)
#             # bot.send_reply_message(f'pong: {FSM.get_state(chat_id)}', message_id , chat_id)
#         case _: bot.send_message(text, chat_id)

#     return True