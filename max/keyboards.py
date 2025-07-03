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

def test():
    key = list()
    button1 = button_callback('первая', '1')
    button2 = button_callback('вторая', '2')
    button3 = button_callback('третья', '3')
    button4 = button_callback('четвертая', '4')
    key.append([button1, button2])
    key.append([button3, button4])
    
    return key

def empty_keyboard():
    key = list()
    button1 = button_callback('первая', '1')
    key.append([button1])
    return key