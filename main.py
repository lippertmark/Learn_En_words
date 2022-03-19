import telebot
from telebot import types

bot = telebot.TeleBot('тут будет апи ключ')


def sql_new_user(tg_id, tg_username):
    # TODO(@Сергей) сделать запись в БД
    pass


@bot.message_handler(commands=['start'])
def welcome(message):
    pass
    # TODO(@Олеся) написать приветственное сообщение
    # TODO(@Олеся) сделать меню
    # про меню:
    # кнопка СЛОВА: callback_data='words'
    # кнопка ПРОФИЛЬ: callback_data='profile'
    # TODO(@Олеся) обратиться к функции которую сделает @Сергей для создания пользоваетля sql_new_user(tg_id, tg_username)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    username = call.message.chat.username
    if call.message:
        if call.data == 'words':
            pass
            # TODO(@Амир) создать меню типа УЧИТЬ или Повторять
            # описание меню:
            # кнопка УЧИТЬ: callback_data='learn'
            # кнопка ПОВТОРЯТЬ: callback_data='repeat'
        elif call.data == 'words':
            pass
            # TODO(@Амир) организовать выдачу слов
            # пока хз как




    # тут ответы на кнопки


@bot.messege_handler(content_type=['text'])
def text(message):
    pass
    # тут ответы на текст
