import telebot
from config import keys, TOKEN
from extensions import ConvertionException, FiatConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Добро пожаловать! \n' \
            'С помощью этого бота можно легко узнать курс нужной Вам валюты. \n' \
           '1. Введите имя(аббревиатура) валюты c маленькой буквы. \n' \
           '2. Через пробел введите в какую валюту хотите превести. \n' \
           '3. Через пробел введите количество переводимой валюты. \n' \
           '4. Чтобы увидеть весь список валют введите комнду /values. \n' \
           '5. Чтобы узнать рашифровку аббревиатур валют введите команду /help.'

    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'rub - Рубль \n' \
           'eur - Евро \n' \
           'usd - Доллар США \n' \
           'chf - Швейцарский франк \n' \
           'gbp - Фунт стерлингов \n' \
           'jpy - Японская йена \n' \
           'try - Турецкая лира \n' \
           'cny - Китайский юань \n' \
           'byn - Белорусский рубль'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Количество символов введено неверно. \n'
                                      'Для ознакомления введите команду /start.')

        quote, base, amount = values
        total_base = FiatConverter.convert(quote, base, amount)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')

    else:
        text = f'{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)

bot.polling()