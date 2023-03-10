import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = 'TOKEN'
API_KEY = 'API_KEY'
URL_WEATHER_API = 'https://api.openweathermap.org/data/2.5/weather'

EMOJI_CODE = {200: 'β',
              201: 'β',
              202: 'β',
              210: 'π©',
              211: 'π©',
              212: 'π©',
              221: 'π©',
              230: 'β',
              231: 'β',
              232: 'β',
              301: 'π§',
              302: 'π§',
              310: 'π§',
              311: 'π§',
              312: 'π§',
              313: 'π§',
              314: 'π§',
              321: 'π§',
              500: 'π§',
              501: 'π§',
              502: 'π§',
              503: 'π§',
              504: 'π§',
              511: 'π§',
              520: 'π§',
              521: 'π§',
              522: 'π§',
              531: 'π§',
              600: 'π¨',
              601: 'π¨',
              602: 'π¨',
              611: 'π¨',
              612: 'π¨',
              613: 'π¨',
              615: 'π¨',
              616: 'π¨',
              620: 'π¨',
              621: 'π¨',
              622: 'π¨',
              701: 'π«',
              711: 'π«',
              721: 'π«',
              731: 'π«',
              741: 'π«',
              751: 'π«',
              761: 'π«',
              762: 'π«',
              771: 'π«',
              781: 'π«',
              800: 'β',
              801: 'π€',
              802: 'β',
              803: 'β',
              804: 'β'}

bot = telebot.TeleBot(TOKEN)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('ΠΠΎΠ»ΡΡΠΈΡΡ ΠΏΠΎΠ³ΠΎΠ΄Ρ', request_location=True))
keyboard.add(KeyboardButton('Π ΠΏΡΠΎΠ΅ΠΊΡΠ΅'))


def get_weather(lat, lon):
    params = {'lat': lat,
              'lon': lon,
              'lang': 'ru',
              'units': 'metric',
              'appid': API_KEY}
    response = requests.get(url=URL_WEATHER_API, params=params).json()
    city_name = response['name']
    description = response['weather'][0]['description']
    code = response['weather'][0]['id']
    temp = response['main']['temp']
    temp_feels_like = response['main']['feels_like']
    humidity = response['main']['humidity']
    emoji = EMOJI_CODE[code]
    message = f'π ΠΠΎΠ³ΠΎΠ΄Π° Π²: {city_name}\n'
    message += f'{emoji} {description.capitalize()}.\n'
    message += f'π‘ Π’Π΅ΠΌΠΏΠ΅ΡΠ°ΡΡΡΠ° {temp}Β°C.\n'
    message += f'π‘ ΠΡΡΡΠ°Π΅ΡΡΡ {temp_feels_like}Β°C.\n'
    message += f'π§ ΠΠ»Π°ΠΆΠ½ΠΎΡΡΡ {humidity}%.\n'
    return message


@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = 'ΠΡΠΏΡΠ°Π²Ρ ΠΌΠ½Π΅ ΡΠ²ΠΎΠ΅ ΠΌΠ΅ΡΡΠΎΠΏΠΎΠ»ΠΎΠΆΠ΅Π½ΠΈΠ΅ ΠΈ Ρ ΠΎΡΠΏΡΠ°Π²Π»Ρ ΡΠ΅Π±Π΅ ΠΏΠΎΠ³ΠΎΠ΄Ρ.'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def send_weather(message):
    lon = message.location.longitude
    lat = message.location.latitude
    result = get_weather(lat, lon)
    bot.send_message(message.chat.id, result, reply_markup=keyboard)


@bot.message_handler(regexp='Π ΠΏΡΠΎΠ΅ΠΊΡΠ΅')
def send_about(message):
    text = 'ΠΠΎΡ ΠΏΠΎΠ·Π²ΠΎΠ»ΡΠ΅Ρ ΠΏΠΎΠ»ΡΡΠΈΡΡ ΠΏΠΎΠ³ΠΎΠ΄Ρ Π² ΡΠ΅ΠΊΡΡΠ΅ΠΌ ΠΌΠ΅ΡΡΠΎΠΏΠΎΠ»ΠΎΠΆΠ΅Π½ΠΈΠΈ!\n'
    text += 'ΠΠ»Ρ ΠΏΠΎΠ»ΡΡΠ΅Π½ΠΈΡ ΠΏΠΎΠ³ΠΎΠ΄Ρ - ΠΎΡΠΏΡΠ°Π²Ρ Π±ΠΎΡΡ Π³Π΅ΠΎΠΏΠΎΠ·ΠΈΡΠΈΡ.\n'
    text += 'ΠΠΎΠ³ΠΎΠ΄Π° Π±Π΅ΡΠ΅ΡΡΡ Ρ ΡΠ°ΠΉΡΠ° https://openweathermap.org.\n'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


bot.infinity_polling()
