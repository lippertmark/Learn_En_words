import telebot
from telebot import types
import sqlite3
import random

bot = telebot.TeleBot('5162531568:AAFulbpqupsSMHiri53UD0jIRC7gpzUayTc')
GENERATED = 'GENERATED'
RETRY = 'RETRY'
DONE = 'DONE'


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
    if sql_notes_by_user_and_word(tg_id, word_id) != []:  # надо не как с классом
        return True
    return False


def generate_word(tg_id):
    '''
    Генерирует новое слово, проверяя его на то что оно уже выучено, если выучено то генерируется новое.
    :param tg_id:
    :return: word (tuple): (word_id, word_en, word_ru, category, sentance, hate)
    '''
    # TODO (@Олеся)
    word = random.choice(sql_all_words())
    if is_learned(tg_id, word.word_id):  # надо не как с классом
        generate_word(tg_id)
    else:
        return word


def send_new_word(tg_id):
    '''
    Генерирует новое слово
    Отправляет юзеру это слово
    :param tg_id:
    :return:
    '''
    # TODO (@Олеся) модификация не больше 10 слов
    word = generate_word(tg_id)
    bot.send_message(chat_id=tg_id.from_user.id, text=f'{word.word_en}')  # добавить предложение
    new_note(tg_id, word_id, GENERATED, None)
    # TODO (@Олеся) добавить инлайнкейборд для выбора правильного варианта


@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    user_username = message.from_user.username
    sticker = open('img/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    markup = telebot.types.InlineKeyboardMarkup()
    item1 = telebot.types.InlineKeyboardButton(text='Профиль🗂', callback_data='profile')
    item2 = telebot.types.InlineKeyboardButton(text='Учить новые слова🔎', callback_data='learn_new')
    item3 = telebot.types.InlineKeyboardButton(text='Повторять слова📚', callback_data='repeat_words')

    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id,
                     'Привет, {0.first_name}!🥰\nЯ - <b>{1.first_name}</b>, бот для изучения английского языка.🤖'.format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)
    sql_new_user(user_id, user_username)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if sql_is_user_in_db(call.message.from_user.id):
        username = call.message.chat.username
        # TODO (@Олеся) проверка на существование юзера
        if call.message:
            if call.data == 'profile':
                markup2 = telebot.types.InlineKeyboardMarkup()
                markup2.add(telebot.types.InlineKeyboardButton(text='Учить новые слова🔎', callback_data='learn_new'))
                markup2.add(telebot.types.InlineKeyboardButton(text='Повторять слова📚', callback_data='repeat_words'))

                achive = '✅' * sql_user_info(call.message.from_user.id).score  # надо не как с классом
                bot.send_message(call.message.chat.id,
                                 f'Ваш ник: {username}\n\nАктивность за 10 дней: {achive}\n\nВыученных слов: {sql_user_info(call.message.from_user.id).cnt_words_total}',
                                 reply_markup=markup2)
            elif call.data == 'learn_new':
                # TODO (@Олеся) вызввать нфункцию
                pass
            elif call.data == 'repeat_words':
                pass
            elif call.data == 'wrong':
                # TODO (@Олеся) сделать обработчик вронг, отправка слова
                pass
            elif call.data == 'accept':
                # TODO (@Олеся) сообщение похвала, new_note(tg_id, word_id, RETRY, 0), отправка нового слова
                # TODO (@Олеся) инкриминировать счетчик выученных слов
                pass
        # тут ответы на кнопки


@bot.message_handler(content_type=['text'])
def text(message):
    if sql_is_user_in_db(message.from_user.id):
        # TODO (@Олеся) проверка на существование юзера
        pass
        # тут ответы на текст


bot.polling(none_stop=True)
