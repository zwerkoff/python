commands = [
    ('help', 'Вывод доступных команд бота'),
    ('support', 'Начать общение с оператором техподдержки'),
    ('count', 'Передать показания счётчика'),
    ('info', 'Вывод доступной информации боту о Вашем аккаунте в Max')
]

#для команды help формирую строку с командами
text_commands = """"""
for com, description in commands:
    text_commands += f'/{com} - {description} \n'

def command(name, description):
        """
        Вспомогательный метод для подготовки описаний команд бота и использования в методе edit_bot_info.
        :param name: название команды (например для команды /help => 'help')
        :param description: описание команды
        :return: Возвращает dict команд.
        """
        com = {"name": "/{}".format(name), "description": description}
        return com

def get_commands():
    result = [command(com, description) for com, description in commands]
    return result