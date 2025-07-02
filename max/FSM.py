from typing import *

class FSMStorage(dict):
    
    def __init__(self):
        self.states: dict(int, str) = dict()
        self.data: dict(int, Any) = dict()

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
