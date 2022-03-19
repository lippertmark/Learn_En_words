import telebot
from telebot import types

bot = telebot.TeleBot('тут будет апи ключ')


def sql_new_user(tg_id, tg_username):
    # TODO сделать запись в БД
    pass


@bot.message_handler(commands=['start'])
def welcome(message):
    pass
    # TODO написать приветственное сообщение
    # TODO сделать меню
    # TODO обратиться к функции которую сделает @Сергей для создания пользоваетля sql_new_user(tg_id, tg_username)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    pass
    # тут ответы на кнопки


@bot.messege_handler(content_type=['text'])
def text(message):
    pass
    # тут ответы на текст
