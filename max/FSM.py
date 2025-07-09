from typing import *

class FSMStorage():
    
    def __init__(self):
        self.states: dict(int, str) = dict()
        self.data: dict(int, Any) = dict()
        self.mid: dict(int, dict) = dict()

class FSM:
    
    def __init__(self, storage: FSMStorage, user_id: int):
        self.storage: FSMStorage = storage
        self.user_id: int = user_id

    @property
    def state(self):
        return self.storage.states.get(self.user_id)

    @state.setter
    def state(self, value):
        self.storage.states[self.user_id] = value

    @state.deleter
    def state(self):
        self.storage.states.pop(self.user_id)

    @property
    def data(self):
        return self.storage.data.get(self.user_id)

    @data.setter
    def data(self, value):
        self.storage.data[self.user_id] = value

    @data.deleter
    def data(self):
        self.storage.data.pop(self.user_id)

class MID:

    def __init__(self, storage: FSMStorage, user_id: int):
        self.storage: FSMStorage = storage
        self.user_id: int = user_id

    def add_key_value(self, key, value):
        mid = self.storage.mid.get(self.user_id)
        if not mid:
            self.storage.mid[self.user_id] = dict()
        self.storage.mid[self.user_id][key] = value
    
    def add_mid(self, mid_abonent, mid_operator):
        self.add_key_value(mid_abonent, mid_operator)
        self.add_key_value(mid_operator, mid_abonent)

    def add_abonent_chat_id(self, chat_id):
        self.add_key_value('abonent_chat_id', chat_id)

    def add_operator_chat_id(self, chat_id):
        self.add_key_value('operator_chat_id', chat_id)

    def get_value(self, key):
        return self.storage.mid[self.user_id].get(key)

    def del_mid(self):
        self.storage.mid.pop(self.user_id)

    def __str__(self):
        mid = self.storage.mid.get(self.user_id)
        if mid:
            res = '{\n'
            for key, value in mid.items():
                res += f'{key}  :   {value}\n'
            res += '}'
            return res
        else:
            return None

# storage = FSMStorage()
# mid = MID(storage, 12345)
# mid.add_mid('12345', '54321')

# print(mid)
