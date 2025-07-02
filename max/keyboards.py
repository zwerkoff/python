from api import BotHandler

def test(bot: BotHandler):
    key = list()
    button1 = bot.button_callback('первая', '1')
    button2 = bot.button_callback('вторая', '2')
    button3 = bot.button_callback('третья', '3')
    button4 = bot.button_callback('четвертая', '4')
    key.append([button1, button2])
    key.append([button3, button4])
    
    return key