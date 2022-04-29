import telebot
from telebot import types
import sql.use_sql as sql

import random

LEARN = 5  # константа сколько раз повторить, чтобы выучить
bot = telebot.TeleBot('5162531568:AAFulbpqupsSMHiri53UD0jIRC7gpzUayTc')


def is_learned(tg_id, word_id):
    """
    Проверяет слово выучено пользователем или нет.
    :param tg_id:
    :param word_id:
    :return: true/false
    """
    # TODO (@Олеся)
    if sql.notes_by_user_and_word(tg_id, word_id) != []:  # надо не как с классом
        return True
    return False


def generate_word(tg_id):
    """
    Генерирует новое слово, проверяя его на то что оно уже выучено, если выучено то генерируется новое.
    :param tg_id:
    :return: word (tuple): (word_id, word_en, word_ru, category, sentence, hate)
    """
    # TODO (@Олеся)
    word = random.choice(sql.all_words())
    if is_learned(tg_id, word.word_id):  # надо не как с классом
        generate_word(tg_id)
    else:
        return word


def send_new_word(tg_id):
    """
    Генерирует новое слово
    Отправляет юзеру это слово
    :param tg_id:
    :return:
    """
    # TODO (@Олеся) модификация не больше 10 слов
    word = generate_word(tg_id)
    bot.send_message(chat_id=tg_id.from_user.id, text=f'{word.word_en}')  # добавить предложение
    sql.new_note(tg_id, word_id, sql.GENERATED, None)
    # TODO (@Олеся) добавить инлайнкейборд для выбора правильного варианта


def generate_choice(word_id):
    """
    Generate 3 wrong answer
    :param word_id:
    :return: list(of 4 tuples(word_id, word_ru, word_en, 1-correct answer, 0-wrong answer))
    """
    # TODO (@Олеся)
    pass


def send_repeat_word(tg_id, word_id):
    """
    Отправляет пользователю слово для повторения.
    :param tg_id:
    :param word_id:
    :return: nothing
    """
    # TODO (@Amir)
    pass


@bot.message_handler(commands=['start'])
def welcome(message):
    # TODO (@Олеся) добавить проверку на существование юзера также как в остальных
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
    sql.new_user(user_id, user_username)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if sql.is_user_in_db(call.message.from_user.id):
        username = call.message.chat.username
        tg_id = call.message.from_user.id
        if call.message:
            if call.data == 'profile':
                markup2 = telebot.types.InlineKeyboardMarkup()
                markup2.add(telebot.types.InlineKeyboardButton(text='Учить новые слова🔎', callback_data='learn_new'))
                markup2.add(telebot.types.InlineKeyboardButton(text='Повторять слова📚', callback_data='repeat_words'))

                achieve = '✅' * sql.user_info(tg_id).score  # надо не как с классом
                bot.send_message(tg_id,
                                 f'Ваш ник: {username}\n\nАктивность за 10 дней: {achieve}\n\nВыученных слов: '
                                 f'{sql.user_info(tg_id).cnt_words_total}',
                                 reply_markup=markup2)
            elif call.data == 'learn_new':
                # TODO (@Олеся) вызввать функцию send_new_word
                pass
            elif call.data == 'repeat_words':
                # TODO (@Amir)
                # используешь фцнкцию notes_by_user фильтр по RETRY и again < LEARN
                # выдать слово send_repeat_word
                pass
            elif call.data == 'wrong':
                # TODO (@Олеся) сделать обработчик вронг, отправка слова
                pass
            elif call.data == 'accept':
                # TODO (@Олеся) сообщение похвала
                # new_note(tg_id, word_id, RETRY, 0)
                # отправка нового слова
                # TODO (@Олеся) инкриминировать счетчик выученных слов
                pass
        # тут ответы на кнопки


@bot.message_handler(content_type=['text'])
def text(message):
    if sql.is_user_in_db(message.from_user.id):
        pass
        print()
        # TODO (@Amir)
        # 1. либо похвола с кнопкой Повторять дальше(callback_data='repeat_words')
        # - добавить ноту с again+1
        # - в базе данных User repeat_word_id set NULL
        # 2. либо просим ввести заново
        # тут ответы на текст
    else:
        pass
        # TODO (@Олеся) нужно сказать напиши /start


bot.polling(none_stop=True)
