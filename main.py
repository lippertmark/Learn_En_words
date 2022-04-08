import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('5162531568:AAFulbpqupsSMHiri53UD0jIRC7gpzUayTc')


def sql_new_user(tg_id, tg_username):
    """
    Функция реализует создание записи в базе данных о пользователе
    :param tg_id:
    :param tg_username:
    :return: nothing
    """
    conn = sqlite3.connect('EnglishBotka.db')
    cursor = conn.cursor()
    req = f"INSERT INTO User VALUES ({tg_id}, '{tg_username}', 0)"
    cursor.execute(req)
    conn.close()


def sql_is_user_in_db(tg_id):
    """
    Функциф проверяет создан существует ли уже такой юзер в базе данных
    :param tg_id:
    :return: true/false
    """
    conn = sqlite3.connect('EnglishBotka.db')
    cursor = conn.cursor()
    req = f"SELECT tg_id FROM User"
    cursor.execute(req)
    result = cursor.fetchall()
    conn.close()
    for i in result:
        if tg_id in i:
            return True
    return False


def sql_all_words():
    '''
    Функция вытаскивает список слов всех из базы данных.
    :return: all_words (list of touple(word_id, word_en, category, word_ru, sentance, hate)):
        лист всех слов из кортежей со всеми параметрам
    '''
    # TODO (@Сергей)
    pass


def sql_notes_by_user(tg_id):
    '''
    Выдает все записи о юзере из базы данных Note.
    :param tg_id: telegram user id
    :return: notes_by_user (list of tuples): (tg_id, date, word_id, type, again)
    '''
    # TODO (@Сергей)
    pass


def sql_notes_by_user_and_word(tg_id, word_id):
    '''
    Выдает записи о юзере с конкретном словом.

    :param tg_id:
    :param word_id:
    :return: notes_user_word list(of tuples): (tg_id, date, word_id, type, again)
    '''
    # TODO (@Сергей)
    pass


def sql_user_is_exist(tg_id):
    '''
    Проверяет существует ли такой пользвователь.
    :param tg_id:
    :return: true/false
    '''
    # TODO (@Сергей)
    pass


def sql_user_info(tg_id):
    '''
    Выдает информацию о юзере.
    :param tg_id:
    :return:
        user info (dict): Словарь с ключами tg_id, tg_username, score, cnt_words_today, cnt_words_total
    '''
    # TODO (@Сергей)
    pass


def is_learned(tg_id, word_id):
    '''
    Проверяет слово выучено пользователем или нет.
    :param tg_id:
    :param word_id:
    :return: true/false
    '''
    # TODO (@Олеся)
    pass


def generate_word(tg_id):
    '''
    Генерирует новое слово, проверяя его на то что оно уже выучено, если выучено то генерируется новое.
    :param tg_id:
    :return: word (tuple): (word_id, word_en, word_ru, category, sentance, hate)
    '''
    # TODO (@Олеся)
    pass


def send_new_word(tg_id):
    '''
    Генерирует новое слово
    Отправляет юзеру это слово
    :param tg_id:
    :return:
    '''
    # TODO (@Олеся)
    pass


@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    user_username = message.from_user.username
    sticker = open('img/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Профиль')
    item2 = types.KeyboardButton('Учить новые слова')
    item3 = types.KeyboardButton('Повторять слова')

    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id,
                     'Привет, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот для изучения английского языка.'.format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)
    sql_new_user(user_id, user_username)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    username = call.message.chat.username
    # TODO (@Олеся) проверка на существование юзера
    if call.message:
        pass

    # тут ответы на кнопки


@bot.message_handler(content_type=['text'])
def text(message):
    # TODO (@Олеся) проверка на существование юзера
    pass
    # тут ответы на текст


bot.polling(none_stop=True)
