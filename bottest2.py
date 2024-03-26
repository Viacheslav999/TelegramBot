import telebot
from telebot import types
import random
import requests
import json
import os 
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
API = os.getenv('API')


@bot.message_handler(commands=['weather'])
def weather(message):
    """Weather forecast"""
    answer_message = bot.send_message(
        message.chat.id, 'Введите название города.')
    bot.register_next_step_handler(answer_message, get_weather)


def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    data = json.loads(res.content)
    sent_message = bot.reply_to(message, f'Сейчас погода: {
                                data['main']['temp']}')
    bot.register_next_step_handler(sent_message, games)


@bot.message_handler(commands=['start'])
def uf(message):
    """Launch the bot using the command"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('Поздороваться')
    markup.add(btn)
    bot.send_message(message.from_user.id,
                     "Привет!-Я твой бот помощник!", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    """Bot menu"""
    if message.text == 'Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Орел и Решка')
        btn2 = types.KeyboardButton('Рандомные числа')
        btn3 = types.KeyboardButton('Список фильмов')
        btn4 = types.KeyboardButton('Прогноз погоды')
        markup.add(btn1, btn2, btn3, btn4)

        sent_message = bot.send_message(
            message.from_user.id, 'Выберите функцию', reply_markup=markup)
        bot.register_next_step_handler(sent_message, games)


def games(message):
    """Games in the bot and a list of recommended films"""
    if message.text == 'Орел и Решка':

        mylist = ["Орел", "Решка"]
        choice = random.choice(mylist)
        sent_message = bot.send_message(message.chat.id, f"Вам выпало: <u>{
            choice}</u>", parse_mode="html")
        bot.register_next_step_handler(sent_message, games)
    elif message.text == 'Рандомные числа':
        number = random.randint(1, 100)
        sent_message = bot.send_message(message.chat.id, f"Вам выпало: <b>{
            number}</b>", parse_mode="html")
        bot.register_next_step_handler(sent_message, games)
    elif message.text == 'Список фильмов':

        films = [
            {
                'название': 'Форрест Гамп',
                'год выпуска': 1994,
                'режиссер': 'Роберт Земекис'
            },
            {
                'название': 'Побег из Шоушенка',
                'год выпуска': 1994,
                'режиссер': 'Фрэнк Дарабонт'
            },
            {
                'название': 'Звёздные войны',
                'год выпуска': 1977,
                'режиссер': 'Джордж Лукас'
            },

        ]

        def get_movie_list():
            movie_list = ""
            for film in films:
                movie_list += f"Название: {film['название']}\n"
                movie_list += f"Год выпуска: {film['год выпуска']}\n"
                movie_list += f"Режиссер: {film['режиссер']}\n\n"
            return movie_list

        sent_message = bot.send_message(message.chat.id, get_movie_list())
        bot.register_next_step_handler(sent_message, games)

    elif message.text == 'Прогноз погоды':
        weather(message)


bot.polling(none_stop=True)
