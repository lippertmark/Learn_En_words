import telebot
from telebot import types

bot = telebot.TeleBot('тут будет апи ключ')


def sql_new_user(tg_id, tg_username):
    '''
    Функция реализует создание записи в базе данных о пользователе
    :param tg_id:
    :param tg_username:
    :return: nothing
    '''
    # TODO(@Сергей) реализовать
    pass

def sql_is_user_in_db(tg_id):
    '''
    Функциф проверяет создан существует ли уже такой юзер в базе данных
    :param tg_id:
    :return: true/false
    '''
    # TODO(@Сергей) реализовать
    pass

@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    user_username = message.from_user.username
# TODO(@Олеся) написать приветственное сообщение
    sticker = open('img/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
     # в общем, у меня плохо с речью и приветствиями,
    # я накалякаю, а потом исправим на нормальное приветствие
# TODO(@Олеся) сделать меню
    # про меню:
    # кнопка СЛОВА: callback_data='words'
    # кнопка ПРОФИЛЬ: callback_data='profile'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Профиль')
    item2 = types.KeyboardButton('Учить новые слова')
    item3 = types.KeyboardButton('Повторять слова')

    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот для изучения английского языка.'.format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

    # TODO(@Олеся) обратиться к функции которую сделает @Сергей для создания пользоваетля sql_new_user(tg_id, tg_username)
    sql_new_user(user_id, user_username)

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
