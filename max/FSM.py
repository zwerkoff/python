from typing import *

class FSMStorage():
    """
    класс для работы с состояниями и временными данными пользователей.

    Создаётся при инициализации бота. Обращение к нему: bot.storage
    """
    
    def __init__(self):
        self.states: dict(int, str) = dict()
        self.data: dict(int, Any) = dict()

class FSM:
    """
    класс для работы с состоянием конкретного юзера и его временными данными.

    Параметры:
    storage - Экземпляр FSMStorage.  
    user_id - id абонента в мессенджере
    Состояние хранится в FSMStorage.state. Может быть только строкой
    Данные хранятся в FSMStorage.data. Может быть любым типом. Если тип dict, то для работы с ним есть отдельные методы 
    """
    
    def __init__(self, storage: FSMStorage, user_id: int):
        self.storage: FSMStorage = storage
        self.user_id: int = user_id

    @property
    def state(self):
        """
        получение текущего состояния юзера

        Возвращает None если нет состояния
        """
        return self.storage.states.get(self.user_id)

    @state.setter
    def state(self, value):
        """
        Присвоение нового состояния юзера
        """
        self.storage.states[self.user_id] = value

    @state.deleter
    def state(self):
        """
        Удаляет состояние юзера
        """
        self.storage.states.pop(self.user_id)

    @property
    def data(self):
        """
        получение временных данных юзера

        Возвращает None если нет данных
        """
        return self.storage.data.get(self.user_id)

    @data.setter
    def data(self, value):
        """
        Присвоение новых данных юзера
        """
        self.storage.data[self.user_id] = value

    @data.deleter
    def data(self):
        """
        Удаляет все данные юзера
        """
        self.storage.data.pop(self.user_id)

    # Методы для работы с data, если в качестве значения будет использоваться словарь

    def add_key_and_value(self, key, value):
        """
        Добавление данных в data, если нужно использовать словарь
        
        key = имя ключа в словаре.
        value = значание, которое примет ключ
        """
        if not isinstance(self.data, dict):
            self.data = dict()
        self.data[key] = value

    def add_abonent_info(self, chat_id, id):
        """
        Для функции talking_to_support.

        Добавляет в data id абонента и id чата абонента и бота
        """
        self.add_key_and_value('abonent_chat_id', chat_id)
        self.add_key_and_value('abonent_id', id)

    def add_operator_info(self, chat_id, id):
        """
        Для функции talking_to_support.

        Добавляет в data id оператора поддерки и id чата оператора и бота
        """
        self.add_key_and_value('operator_chat_id', chat_id)
        self.add_key_and_value('operator_id', id)

    def add_mid(self, mid1, mid2):
        """
        Для функции talking_to_support

        Добавляет в data два ключа: 
        mid1 с значением mid2 и
        mid2 с значением mid1
        необходимо чтобы находит сообщения, которые пользователь или оператор правит, пересылает или удаляет во время общения с поддеркой

        mid1:   message_id отправленного сообщения от юзера боту и 
        mid2:   message_id сообщения, которое переслал бот в поддержку(или абоненту) 
        """
        self.add_key_and_value(mid1, mid2)
        self.add_key_and_value(mid2, mid1)

    def get_data(self, key):
        """
        Получение значения ключа key из data
        
        key = ключ из словаря data. Ключ и его значение добавляются методом add_key_and_value
        :return: возвращает значение ключа, если он есть. Иначе None.
        """
        return self.data.get(key) if isinstance(self.data, dict) else None

    def get_abonent_chat_id(self):
        """
        Для функции talking_to_support

        Получение id чата абонента и бота
        """
        return self.data.get('abonent_chat_id') if isinstance(self.data, dict) else None

    def get_abonent_id(self):
        """
        Для функции talking_to_support

        Получение id абонента
        """
        return self.data.get('abonent_id') if isinstance(self.data, dict) else None

    def get_operator_chat_id(self):
        """
        Для функции talking_to_support

        Получение id чата оперетора и бота
        """
        return self.data.get('operator_chat_id') if isinstance(self.data, dict) else None

    def get_operator_id(self):
        """
        Для функции talking_to_support

        Получение id оператора
        """
        return self.data.get('operator_id') if isinstance(self.data, dict) else None
