# Модуль для работы с базами данных
# brew install sqlite
# brew install --cask db-browser-for-sqlite
import sqlite3
import os

DATABASE_MODELS = 'models.sq3'


def split_models_output():
    """Функция для нарезания файла с моделями в массив данных"""
    list_ = []
    file = 'models_output.txt'
    with open(file, 'r') as file:
        for item in file:
            string_ = item[:-1].split('~')
            list_.append(string_)
    if [] in list_:
        list_.remove([])
    return list_


MODELS_DATA = split_models_output()


def create_db():
    """Функция создания базы данных с моделями"""
    os.remove(DATABASE_MODELS)

    # Подключаемся к базе и создаем поля
    connection = sqlite3.connect(DATABASE_MODELS)
    cur = connection.cursor()

    sqlite_create_table_query = '''
    CREATE TABLE IF NOT EXISTS models (
    name TEXT PRIMARY KEY NOT NULL,
    role TEXT DEFAULT model NOT NULL,
    activity TEXT DEFAULT active NOT NULL,
    priority INT DEFAULT 3 NOT NULL,
    try INTEGER DEFAULT 1,
    avatar BLOB
    );'''

    # Создаем таблицу
    cur.execute(sqlite_create_table_query)

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    cur.close()


def insert_data_in_table():
    """Функция вставки данных в таблицу из специально подготовленного файла"""
    connection = sqlite3.connect(DATABASE_MODELS)
    cursor = connection.cursor()

    sqlite_inserting_data_in_table_query = '''
    INSERT INTO models (name, role, activity, priority)
    VALUES (?, ?, ?, ?)
    '''

    for item in MODELS_DATA:
        name, type_model, activ, property_ = item
        cursor.execute(sqlite_inserting_data_in_table_query,
                       [name, type_model, activ, property_])

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    cursor.close()


def read_db():
    """Функция чтения из базы данных"""
    connection = sqlite3.connect(DATABASE_MODELS)
    cursor = connection.cursor()

    cursor.execute("""SELECT name, role, activity, priority FROM models 
    WHERE activity == 'active'
    ORDER BY priority
    """)  # получение данных из таблицы если модель активна
    rows = cursor.fetchall()

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    cursor.close()

    return rows


DATABASE_CONTENT = read_db()


if __name__ == '__main__':
    # create_db()
    # insert_data_in_table()
    print(read_db())
