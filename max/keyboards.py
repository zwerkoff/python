def _button_callback(text, payload, intent='default'):
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

def _attach_buttons(buttons):
        """
        Метод подготовки к отправке кнопок в качестве элемента attachments
        :param buttons: кнопки в формате списка, cформированные при помощи:
            button_callback, button_contact, button_link, button_location и т.д.
        :return attach: подготовленный контент
        """
        # self.typing_on(self.get_chat_id())
        attach = None
        if isinstance(buttons, list):
            try:
                if buttons[0][0]:
                    attach = [{"type": "inline_keyboard",
                               "payload": {"buttons": buttons}
                               }
                              ]
            except Exception as e:
                attach = [{"type": "inline_keyboard",
                           "payload": {"buttons": [buttons]}
                           }
                          ]
                logger.info('atach_button is list, except (%s)', e)
        else:
            attach = [{"type": "inline_keyboard",
                       "payload": {"buttons": [[buttons]]}
                       }
                      ]
        return attach

############################
# Клавиатуры
def request_support():
    
    buttons = list()
    button1 = _button_callback('Начать диалог с абонентом', 'start_support')
    buttons.append([button1])
    
    return _attach_buttons(buttons)

