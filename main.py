import telebot
from config import *
from extensions import Converter, APIException


bot = telebot.TeleBot(TOKEN)  # инициализация объекта бота


@bot.message_handler(commands=['start', 'help'])  # обработчик команд start/help
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n <название исходной валюты> \
 <название валюты, в которую нужно перести> <количество переводимой валюты> \n Увидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])  # обработчик команды values
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in exchanges.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])  # обработчик вводимого текста
def convert(message: telebot.types.Message):

    try:
        values = message.text.split()

        if len(values) != 3:
            raise APIException('Указано неверное количество параметров')

        base, sym, amount = values
        new_price = Converter.get_price(base, sym, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя: \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка в команде :\n{e}')
    else:
        text = f'Цена {amount} {base} в {sym} = {new_price}'
        bot.reply_to(message, text)


bot.polling()
