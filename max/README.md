# Два класса. Первый FSMStorage - создает экземпляр хранилища. 
# Можно добавить в класс BotHandler в метод __init__ строку: -->
    self.storage: FSMStorage = FSMStorage() 
# и хранилище будет создаваться при создании экземпляра бота. Затем бращаться к нему. Например:
# создаем бота: 
    bot = BotHandler(TOKEN)
# обращаемся к хранилищу: 
    storage = bot.storage

# В хранилище два подхранилища: 
    state - принимает и возвращает "состояние" пользователя. (только str)
    data - принимает и возвращает любые данные пользователя. (любой тип данных)

# Втрой класс - FSM. Необходим для работы с состоянием конкретного пользователя. 
# 2 обязательных параметра: общее хранилище состояний и id пользователя в Max
# Создаем экземпляр класса:
    sergei = FSM(bot.storage, user_id)

# Получаем состояние пользователя:
    print(sergei.state)
    Вывод None если не задано состояние

# Задаем состояние:
    sergei.state = 'wait_support'
    print(sergei.state)
    Вывод: 'wait_support'

# Удаляем состояние:
    del sergei.state
    print(sergei.state)
    Вывод: None

# Получаем данные пользователя:
    print(sergei.data)
    Вывод: None

# Задаем данные 
    fio = {
        'f' : 'Ivanov',
        'i' : 'Sergei',
        'o' : 'Ivanovich'
    }
    sergei.data = fio
    print(sergei.data)
    Вывод: {'f': 'Ivanov', 'i': 'Sergei', 'o': 'Ivanovich'}

# Удаляем данные:
    del sergei.data
    print(sergei.data)
    Вывод: None

# Таким же образом можно получать и изменять данные других пользователей, если знаем их id






