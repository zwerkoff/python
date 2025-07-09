from api import BotHandler
from FSM import FSM
from config import SUPPORT
import logging


class Update:

    def __init__(self, bot: BotHandler, upd: dict):
        self.bot = bot
        self.upd = upd
    
    @property
    def chat_id(self):
        return self.bot.get_chat_id(self.upd)

    @property
    def user_id(self):
        return self.bot.get_user_id(self.upd)
    
    @property
    def user_name(self):
        return self.bot.get_name(self.upd)

    @property
    def message_id(self):
        return self.bot.get_message_id(self.upd)

    @property
    def text(self):
        return self.bot.get_text(self.upd)

    @property
    def attachments(self):
        return self.bot.get_attachments(self.upd)

    @property
    def callback_id(self):
        return self.bot.get_callback_id(self.upd)

    @property
    def payload(self):
        return self.bot.get_payload(self.upd)

    @property
    def type_message(self):
        return self.bot.get_update_type(self.upd)

    @property
    def id_link_message(self):
        link_message = self.bot.get_link_message(self.upd)
        if link_message:
            return link_message.get('mid')
        return None

    @property
    def link_type(self):
        return self.bot.get_link_type(self.upd)

    def __str__(self):
        res = '{\n'
        for key, value in self.upd.items():
            res += f'{key}  :   {value}\n'
        res += '}'
        return res
