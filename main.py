import telebot
from telebot import types
import sql.use_sql as sql
import random
LEARN = 5
bot = telebot.TeleBot('5162531568:AAFulbpqupsSMHiri53UD0jIRC7gpzUayTc')
ACCEPT_MESSAGES = ['Правильно, умница! 😎', 'Excellent job! 🥳', 'Молодец, так держать! 🤓']
def is_learned(tg_id, word_id):
    """
    Проверяет слово выучено пользователем или нет.
    :param tg_id:
    :param word_id:
    :return: true(learned)/false(not learned)
    """
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
    if sql.user_info(tg_id)['cnt_words_today'] == 10:
        bot.send_message(chat_id=tg_id, text=f'Сегодня ты уже выучил 10 слов. Возвращайся завтра! 😉')
    else:
        word = generate_word(tg_id)
        sql.add_new_note(tg_id, word[0], sql.GENERATED, None)
        sql.set_new_word_id(tg_id, word[0])
        my_words = generate_choice(word[0])
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text=word[2], callback_data='accept')
        item2 = types.InlineKeyboardButton(text=my_words[1][1], callback_data='wrong')
        item3 = types.InlineKeyboardButton(text=my_words[2][1], callback_data='wrong')
        item4 = types.InlineKeyboardButton(text=my_words[3][1], callback_data='wrong')
        spisok = [item4, item3, item2, item1]
        random.shuffle(spisok)
        for i in spisok:
            markup.add(i)
    bot.send_message(chat_id=tg_id, text=f'Твое слово: {word[1]} 🎓\n\nВыбери правильный вариант ответа:', reply_markup=markup)


def generate_choice(word_id):
    """
    Generate 3 wrong answer
    :param word_id:
    :return: list(of 4 tuples(word_id, word_ru, word_en, 1-correct answer, 0-wrong answer))
    """
    list_of_selected_words = [word_id]
    list_of_words = [(word_id, sql.word_info(word_id)[2], sql.word_info(word_id)[1], 1)]
    while len(list_of_words) < 4:
        wrong_word = random.choice(sql.all_words())
        if wrong_word[0] not in list_of_selected_words:
            list_of_words.append((wrong_word[0], wrong_word[2], wrong_word[1], 0))
            list_of_selected_words.append(wrong_word[0])
    return list_of_words


def generate_repeat_word(tg_id):
    """
    выбирает слово для повторения
    :param tg_id:
    :return: word_id:
    """
    notes = sql.notes_by_user(tg_id)
    all_retry_words = set()
    for note in notes:
        if note[3] == sql.RETRY and note[4] < LEARN:
            all_retry_words.add(note[2])
    all_retry_words = list(all_retry_words)
    repeat_word = random.choice(all_retry_words)
    return repeat_word


def send_repeat_word(tg_id):
    """
    Отправляет пользователю слово для повторения.
    :param tg_id:
    :return: nothing
    """
    word_id = generate_repeat_word(tg_id)
    word = sql.word_info(word_id)
    bot.send_message(chat_id=tg_id, text=f'Введи английский перевод этого слова: {word[2]}')
    sql.set_repeat_word_id(tg_id, word[0])


@bot.message_handler(commands=['start'])
def welcome(message):
    # TODO (@Олеся) добавить проверку на существование юзера также как в остальных
    user_id = message.from_user.id
    user_username = message.from_user.username
    sticker = open('img/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton(text='Профиль 🗂', callback_data='profile')
    item2 = types.InlineKeyboardButton(text='Учить новые слова 🔎', callback_data='learn_new')
    item3 = types.InlineKeyboardButton(text='Повторять слова 📚', callback_data='repeat_words')
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
                                 f'Твой ник 😊: {username}\n\nТвои очки 😋: {score}\n\nВыученных слов 🤌: '
                                 f'{sql.user_info(tg_id)["cnt_words_total"]}',
                                 reply_markup=markup2)
            elif call.data == 'learn_new':
                send_new_word(tg_id)
            elif call.data == 'repeat_words':
                send_repeat_word(tg_id)
            elif call.data == 'wrong':
                bot.send_message(tg_id,
                                 'Не верно, но не расстраивайся, в следующий раз все получится! 😚')
                send_new_word(tg_id)
            elif call.data == 'accept':
                bot.send_message(tg_id,
                                 'Правильный ответ! Умница! 🥰')
                #sql.add_new_note(tg_id, sql.user_info(tg_id)['new_word_id'], sql.RETRY, 0)
                sql.update_note(tg_id, sql.user_info(tg_id)['new_word_id'], type=sql.RETRY, again=0)
                send_new_word(tg_id)
                sql.inc_cnt_today(tg_id)


@bot.message_handler(content_types=['text'])
def lalala(message):
    tg_id = message.from_user.id
    if sql.is_user_in_db(tg_id):
        user = sql.user_info(tg_id)
        repeat_word_id = user['repeat_word_id']
        eng = sql.word_info(repeat_word_id)
        if message.text == eng[1]:
            bot.send_message(chat_id=tg_id, text=random.choice(ACCEPT_MESSAGES))
            sql.inc_again_retry_word(tg_id, repeat_word_id)
            sql.set_repeat_word_id(tg_id, 0)
            send_repeat_word(tg_id)
        else:
            bot.send_message(chat_id=tg_id, text='Попробуй ввести снова 🥺')
    else:
        bot.send_message(message.chat.id, 'Напиши "/start", чтобы начать пользоваться ботом! ✨')
        # TODO (@Олеся) нужно сказать напиши /start


bot.polling(none_stop=True)
# тууган туган як
