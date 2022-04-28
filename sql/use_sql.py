import sqlite3


def new_user(tg_id, tg_username):
    """
    Функция реализует создание записи в базе данных о пользователе
    :param tg_id:
    :param tg_username:
    :return: nothing
    """
    conn = sqlite3.connect('sql/EnglishBotka.db')
    cursor = conn.cursor()
    req = f"INSERT INTO User VALUES ({tg_id}, '{tg_username}', 0, 0, 0)"
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
    for i in result:
        if i[0] == tg_id:
            return i


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
    for i in result:
        if i[0] == tg_id and i[2] == word_id:
            return i


def user_info(tg_id):
    """
    Выдает информацию о юзере.
    :param tg_id:
    :return:
        user info (dict): Словарь с ключами tg_id, tg_username, score, cnt_words_today, cnt_words_total
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
            return d

