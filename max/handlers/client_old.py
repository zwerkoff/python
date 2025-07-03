from api import BotHandler
from FSM import FSM
import keyboards
from time import sleep

def handler(bot: BotHandler, upd: dict):

    user_id = bot.get_user_id(upd)
    fsm = FSM(bot.storage, user_id) 
    chat_id = bot.get_chat_id(upd)
    text = bot.get_text(upd)
    message_id = bot.get_message_id(upd)
    type_message = bot.get_update_type(upd)
    commands = bot.get_bot_commands()
    commands = [f"/{i['name']}" for i in commands]

    # Ловим нажатие на клавитатуру
    if type_message == 'message_callback':
        callback_id = bot.get_callback_id(upd)
        payload = bot.get_payload(upd)
        
        match payload:
            case '1': 
                fsm.state = 'press 1'
                bot.send_message(f'вы нажали {payload}. Вы в состоянии {fsm.state}. Ваши данные в хранилище: {fsm.data}', chat_id)
            case '2':
                fsm.data = {'count': 12345} 
                bot.send_message(f'вы нажали {payload}. Вы в состоянии {fsm.state}. Ваши данные в хранилище: {fsm.data}', chat_id)
            case '3': 
                if fsm.data:
                    del fsm.data
                if fsm.state:
                    del fsm.state
                bot.send_message(f'вы нажали {payload}. Вы в состоянии {fsm.state}. Ваши данные в хранилище: {fsm.data}', chat_id)
            case _:
                image = bot.attach_image('tort.jpg')
                key = bot.attach_buttons(keyboards.test())
                
                bot.edit_message(message_id, 'ТЕКСТ ИЗМЕНЁННЫЙ', attachments=[image])
        return True

    # Ловим команды
    if text in commands:
        match text:
            case '/id': bot.send_message(f'Ваш id в max: {user_id}', chat_id)
            case '/help': bot.send_message(f'Доступные команды бота: {bot.get_bot_commands()}', chat_id)
            case '/ping': 
                # key = keyboards.test(bot)
                image = bot.attach_image('tort.jpg')
                key = bot.attach_buttons(keyboards.test())
                attach = image + key
                # for i in attach:
                #     for key, value in i.items():
                #         print(f'{key}, {value}')
                #         if isinstance(value, dict):
                #             for kkey, vvalue in value.items():
                #                 print(f'    {kkey}, {vvalue}')
                # print(f'chat id: {chat_id}')
                bot.send_message('текст начальный', chat_id, attachments=attach)
                # mid = bot.get_message_id(update)
                # fsm.data = mid
                # bot.send_message(f'Ваш id в max: {user_id}', chat_id)
                
            case _: bot.send_message(text, chat_id)
        return True

    # Просто отвечаем на сообщение
    bot.send_forward_message(None, message_id, chat_id)
    attach = bot.get_attachments(upd)
    # for i in attach:
    #     for key, value in i.items():
    #         print(f'{key}, {value}')
    #         if isinstance(value, dict):
    #             for kkey, vvalue in value.items():
    #                 print(f'    {kkey}, {vvalue}')
    bot.send_message('Пересылаю', chat_id, attachments=attach)
    return True


    





