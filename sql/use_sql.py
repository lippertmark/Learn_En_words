import sqlite3

GENERATED = 'GENERATED'
RETRY = 'RETRY'
DONE = 'DONE'


def new_user(tg_id, tg_username):
    """
    Функция реализует создание записи в базе данных о пользователе
    :param tg_id:
    :param tg_username:
    :return: nothing
    """
    conn = sqlite3.connect('sql/EnglishBotka.db')
    cursor = conn.cursor()
    req = f"INSERT INTO User VALUES ({tg_id}, '{tg_username}', 0, 0, 0, 0, 0)"
    cursor.execute(req)
    conn.commit()
    conn.close()


def is_user_in_db(tg_id):
    """
    Функциф проверяет создан существует ли уже такой юзер в базе данных
    :param tg_id:
    :return: true/false
    """
    conn = sqlite3.connect('sql/EnglishBotka.db')
    cursor = conn.cursor()
    req = f"SELECT tg_id FROM User"
    cursor.execute(req)
    result = cursor.fetchall()
    conn.close()
    for i in result:
        if tg_id in i:
            return True
    return False


def all_words():
    """
    Функция вытаскивает список слов всех из базы данных.
    :return: all_words (list of touple(word_id, word_en, category, word_ru, sentance, hate)):
        лист всех слов из кортежей со всеми параметрам
    """
    conn = sqlite3.connect('sql/EnglishBotka.db')
    cursor = conn.cursor()
    req = f"SELECT * FROM word"
    cursor.execute(req)
    result = cursor.fetchall()

    conn.close()
    return result


def notes_by_user(tg_id):
    """
    Выдает все записи о юзере из базы данных Note.
    :param tg_id: telegram user id
    :return: notes_by_user (list of tuples): (tg_id, date, word_id, type, again)
    """
    conn = sqlite3.connect('sql/EnglishBotka.db')
    cursor = conn.cursor()
    req = f"SELECT * FROM Note"
    cursor.execute(req)
    result = cursor.fetchall()
    conn.close()
    list = []
    for i in result:
        if i[0] == tg_id:
            list.append(i)
    return list


def notes_by_user_and_word(tg_id, word_id):
    """
    Выдает записи о юзере с конкретном словом.
    :param tg_id:
    :param word_id:
    :return: notes_user_word list(of tuples): (tg_id, date, word_id, type, again)
    """
    conn = sqlite3.connect('sql/EnglishBotka.db')
    cursor = conn.cursor()
    req = f"SELECT * FROM Note"
    cursor.execute(req)
    result = cursor.fetchall()
    conn.close()
    list = []
    for i in result:
        if i[0] == tg_id and i[2] == word_id:
            list.append(i)
    return list


def user_info(tg_id):
    """
    Выдает информацию о юзере.
    :param tg_id:
    :return:
        user info (dict): Словарь с ключами tg_id, tg_username, score, cnt_words_today, cnt_words_total, new_word_id, repeat_word_id
    """

    conn = sqlite3.connect('sql/EnglishBotka.db')

    d = dict()
    cursor = conn.cursor()
    req = f"SELECT * FROM User"
    cursor.execute(req)
    result = cursor.fetchall()
    conn.close()
    for i in result:
        if i[0] == tg_id:
            d['tg_id'] = i[0]
            d['tg_username'] = i[1]
            d['score'] = i[2]
            d['cnt_words_today'] = i[3]
            d['cnt_words_total'] = i[4]
            d['new_word_id'] = i[5]
            d['repeat_word_id'] = i[6]
            return d

def set_new_word_id(tg_id, word_id):
    """
    Записывает в базе данных в таблицу User по tg_id в поле new_word_id значение word_id
    :param tg_id:
    :param word_id:
    :return:
    """
    conn = sqlite3.connect('sql/EnglishBotka.db')
    cursor = conn.cursor()
    req = f"UPDATE User SET new_word_id = {word_id} WHERE tg_id = {tg_id}"
    cursor.execute(req)
    conn.commit()
    conn.close()


def set_repeat_word_id(tg_id, word_id):
    """
    Записывает в базе данных в таблицу User по tg_id в поле repeat_word_id значение word_id
    :param tg_id:
    :param word_id:
    :return:
    """
    conn = sqlite3.connect('sql/EnglishBotka.db')
    cursor = conn.cursor()
    req = f"UPDATE User SET repeat_word_id = {word_id} WHERE tg_id = {tg_id}"
    cursor.execute(req)
    conn.commit()
    conn.close()

def add_new_word(word_en, word_ru, category, sentence, hate=0):
    """
    Записывает слово в базу данныз Word
    :param word_en: word in English
    :param word_ru: word in Russian
    :param category: category
    :param sentence: sentence which have this word
    :param hate: how many people have set dislike
    :return: nothing
    """
    conn = sqlite3.connect('sql/EnglishBotka.db')
    cursor = conn.cursor()
    req = f"INSERT INTO Word(word_en, word_ru, category, sentance, hate)" \
          f" VALUES ('{word_en}', '{word_ru}', '{category}', '{sentence}', {hate})"
    print(req)
    cursor.execute(req)
    conn.commit()
    conn.close()


def inc_cnt_today(tg_id, n=1):
    """
    Инкременировать кол-во изученый слов у пользователя на n
    :param n:
    :param tg_id:
    :return:
    """
    conn = sqlite3.connect('sql/EnglishBotka.db')
    cursor = conn.cursor()
    req = f"UPDATE User SET cnt_words_today = cnt_words_today + {n} WHERE tg_id = {tg_id}"
    cursor.execute(req)
    conn.commit()
    conn.close()

def inc_aqain_retry_word(tg_id, word_id):
    """
    Инкременировать кол-во повторений у слова
    :param tg_id:
    :param word_id:
    :return:
    """
    conn = sqlite3.connect('sql/EnglishBotka.db')
    cursor = conn.cursor()
    req = f"UPDATE Note SET again = again + {1} WHERE (tg_id = {tg_id} AND word_id = {word_id} AND type = 'RETRY')"
    cursor.execute(req)
    conn.commit()
    conn.close()


def add_new_note(tg_id, word_id, type, again=0):
    """
    Add new note to data base Note
    :param tg_id: telegram user id
    :param word_id: word id from Word data base
    :param type: type of note
    :param again: how many times person are wrote this word successfully
    :return:
    """
    import datetime
    data = datetime.date.today()
    conn = sqlite3.connect('sql/EnglishBotka.db')
    cursor = conn.cursor()
    req = f"INSERT INTO Note(tg_id, date, word_id, type, again)" \
          f"VALUES ('{tg_id}', '{data}', '{word_id}', '{type}', '{again}')"
    cursor.execute(req)
    conn.commit()
    conn.close()


def notes_with_conditions(db_name, conditions):
    """
    Возвращает все записи, которые подходят под условия.
    :param db_name: Название базы данных
    :param conditions: словарь с условиями
    :return: list of tuples(all columns)
    """
    conn = sqlite3.connect('sql/EnglishBotka.db')
    cursor = conn.cursor()
    req = f"SELECT * FROM {db_name} WHERE {conditions}"
    print(req)
    cursor.execute(req)
    conn.close()
    # думаю


def word_info(word_id):
    """
    Информаци я о словов
    :param word_id:
    :return:
    """
    conn = sqlite3.connect('sql/EnglishBotka.db')
    cursor = conn.cursor()
    req = f"SELECT * FROM Word"
    cursor.execute(req)
    result = cursor.fetchall()
    conn.close()
    for i in result:
        if i[0] == word_id:
            return i

# cond = {
#     'type': RETRY,
#     'word_id': 12,
# }
