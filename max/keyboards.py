def button_callback(text, payload, intent='default'):
        """
        Подготавливает кнопку с реакцией callback
        :param text: подпись кнопки
        :param payload: значение кнопки при нажатии
        :param intent: цвет кнопки
        :return: возвращает подготовленную кнопку для последующего формирования массива
        """
        button = {"type": 'callback',
                  "text": text,
                  "payload": payload,
                  "intent": intent}
        return button

def keyboard_request_support():
    
    key = list()
    button1 = button_callback('Начать диалог с абонентом', 'start_support')
    key.append([button1])
    
    return key

