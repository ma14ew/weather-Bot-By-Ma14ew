import telebot
import requests
import json
import emoji

API = '0c2ddd9b3a1b5aa921482b63338efba0'
API_BOT = '5990480154:AAHoOz-cJ7l55_dABvscVWEuEd_lMNt64SA'

bot = telebot.TeleBot(API_BOT)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,f'Привет! Напиши название города на русском или английском языке и бот тебе покажет краткую информацию о погоде!')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip()
    city_lower = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_lower}&appid={API}&units=metric&lang=ru')
    if res.status_code == 200:
        data = json.loads(res.text)

        if data["main"]["temp"] > 0:
            emoji_tempf = emoji.emojize(':OK_hand:')
        else:
            emoji_tempf = emoji.emojize(':snowman:')

        if data["main"]["feels_like"] > 0:
            emoji_temp = emoji.emojize(':thermometer:')
        else:
            emoji_temp = emoji.emojize(':snowflake:')

        if  data["weather"][0]["description"] == 'дождь':
            emoji_desc = emoji.emojize(':cloud_with_rain:')
        elif data["weather"][0]["description"] == 'пасмурно':
            emoji_desc = emoji.emojize(':cloud:')
        elif data["weather"][0]["description"] == 'облачно с прояснениями':
            emoji_desc = emoji.emojize(':sun_behind_cloud:')
        elif data["weather"][0]["description"] == 'ясно':
            emoji_desc = emoji.emojize(':sun:')
        elif data["weather"][0]["description"] == 'снег':
            emoji_desc = emoji.emojize(':snow:')
        elif data["weather"][0]["description"] == 'небольшая облачность':
            emoji_desc = emoji.emojize(':sun_behind_small_cloud:')
        else:
            emoji_desc = emoji.emojize(':yin_yang:')

        print(data)
        bot.reply_to(message, f'Погода в городе {city}: {data["main"]["temp"]} °C{emoji_tempf}, ощущается как {data["main"]["feels_like"]} °C{emoji_temp}, {data["weather"][0]["description"]}{emoji_desc}')
    else:
        bot.reply_to(message, 'Ошибка, попробуйте ввести правильное название города')

bot.infinity_polling()