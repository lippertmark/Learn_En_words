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
    :return: true(learned)/false(not learned)
    """
    # TODO (@Олеся)
    notes = sql.notes_by_user_and_word(tg_id, word_id)
    if notes == []:
        return False
    elif len(notes) == 1 and notes[0][3] == 'GENERATED':
        return False
    else:
        return True


def generate_word(tg_id):
    """
    Генерирует новое слово, проверяя его на то что оно уже выучено, если выучено то генерируется новое.
    :param tg_id:
    :return: word (tuple): (word_id, word_en, word_ru, category, sentence, hate)
    """
    # TODO (@Олеся)
    flag = 0
    words = sql.all_words()
    while flag == 0:
        word = random.choice(words)
        if not is_learned(tg_id, word[0]):
            flag = 1
    return word


def send_new_word(tg_id):
    """
    Генерирует новое слово
    Отправляет юзеру это слово
    :param tg_id:
    :return:
    """
    # TODO (@Олеся) модификация не больше 10 слов
    if sql.user_info(tg_id)['cnt_words_today'] == 10:
        bot.send_message(chat_id=tg_id, text=f'Ты уже выучил 10 слов на сегодня. Возвращайся завтра!')
    else:
        # добавить предложение
        word = generate_word(tg_id)
        bot.send_message(chat_id=tg_id, text=f'Твое слово: {word[1]}')
        sql.add_new_note(tg_id, word[0], sql.GENERATED, None)
        # TODO (@Олеся) добавить инлайнкейборд для выбора правильного варианта
        my_words = generate_choice(word[0])
        markup = telebot.types.InlineKeyboardMarkup()
        item1 = telebot.types.InlineKeyboardButton(text=word[2], callback_data='accept')
        item2 = telebot.types.InlineKeyboardButton(text=my_words[1][1], callback_data='wrong')
        item3 = telebot.types.InlineKeyboardButton(text=my_words[2][1], callback_data='wrong')
        item4 = telebot.types.InlineKeyboardButton(text=my_words[3][1], callback_data='wrong')
        spisok = [item4, item3, item2, item1]
        random.shuffle(spisok)
        for i in spisok:
            markup.add(i)
    bot.send_message(chat_id=tg_id, text='Выбери правильный вариант ответа:', reply_markup=markup)


def generate_choice(word_id):
    """
    Generate 3 wrong answer
    :param word_id:
    :return: list(of 4 tuples(word_id, word_ru, word_en, 1-correct answer, 0-wrong answer))
    """
    # TODO (@Олеся)
    list_of_selected_words = [word_id]
    list_of_words = [(word_id, sql.word_info(word_id)[2], sql.word_info(word_id)[1], 1)]
    while len(list_of_words) < 4:
        wrong_word = random.choice(sql.all_words())
        if wrong_word[0] not in list_of_selected_words:
            list_of_words.append((wrong_word[0], wrong_word[2], wrong_word[1], 0))
            list_of_selected_words.append(wrong_word[0])
    return list_of_words


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
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    item1 = telebot.types.InlineKeyboardButton(text='Профиль 🗂', callback_data='profile')
    item2 = telebot.types.InlineKeyboardButton(text='Учить новые слова 🔎', callback_data='learn_new')
    item3 = telebot.types.InlineKeyboardButton(text='Повторять слова 📚', callback_data='repeat_words')

    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id,
                     'Привет, {0.first_name}! 🥰\nЯ - <b>{1.first_name}</b>, бот для изучения английского языка. 🤖'.format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)
    if not sql.is_user_in_db(message.from_user.id):
        sql.new_user(user_id, user_username)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    tg_id = call.from_user.id
    if sql.is_user_in_db(tg_id):
        username = call.message.chat.username

        if call.message:
            if call.data == 'profile':
                markup2 = telebot.types.InlineKeyboardMarkup()
                markup2.add(telebot.types.InlineKeyboardButton(text='Учить новые слова 🔎', callback_data='learn_new'))
                markup2.add(telebot.types.InlineKeyboardButton(text='Повторять слова 📚', callback_data='repeat_words'))

                score = sql.user_info(tg_id)['score']
                bot.send_message(tg_id,
                                 f'Ваш ник 😊: {username}\n\nТвои очки 😋: {score}\n\nВыученных слов 🤌: '
                                 f'{sql.user_info(tg_id)["cnt_words_total"]}',
                                 reply_markup=markup2)
            elif call.data == 'learn_new':
                # TODO (@Олеся) вызввать функцию send_new_word
                send_new_word(tg_id)
            elif call.data == 'repeat_words':
                # TODO (@Amir)
                # используешь фцнкцию notes_by_user фильтр по RETRY и again < LEARN
                # выдать слово send_repeat_word
                pass
            elif call.data == 'wrong':
                # TODO (@Олеся) сделать обработчик вронг, отправка слова
                bot.send_message(tg_id,
                                 'Не верно, но не расстраивайся, в следующий раз все получится! 😚')
                send_new_word(tg_id)
            elif call.data == 'accept':
                bot.send_message(tg_id,
                                 'Правильный ответ! Умница! 🥰')
                # TODO (@Олеся) сообщение похвала

                sql.add_new_note(tg_id, sql.user_info(tg_id)['new_word_id'], sql.RETRY, 0)
                send_new_word(tg_id)
                # TODO (@Олеся) инкриминировать счетчик выученных слов
                sql.inc_cnt_today(tg_id)
        # тут ответы на кнопки


@bot.message_handler(content_type=['text'])
def text(message):
    if sql.is_user_in_db(message.from_user.id):
        pass
        # TODO (@Amir)
        # 1. либо похвала с кнопкой Повторять дальше(callback_data='repeat_words')
        # - добавить ноту с again+1
        # - в базе данных User repeat_word_id set NULL
        # 2. либо просим ввести заново
        # тут ответы на текст
    else:
        bot.send_message(message.chat.id, 'Напиши "/start", чтобы начать пользоваться ботом!')
        # TODO (@Олеся) нужно сказать напиши /start


bot.polling(none_stop=True)
# тууган туган як
