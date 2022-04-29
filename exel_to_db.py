import openpyxl, sqlite3
import sql.use_sql as sql


def exel_to_db():
    """
    Добавляет слова из exel файла в базу данных.
    :return:
    """
    book = openpyxl.open("en_words.xlsx", read_only=True)
    sheet = book.active
    cells = sheet['A2':'D10000']
    for word_en, word_ru, category, sentence in cells:
       sql.add_new_word(word_en.value, word_ru.value, category.value, sentence.value)
