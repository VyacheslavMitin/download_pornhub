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


def read_db(priority='all',
            mixed=True):
    """Функция чтения из базы данных"""
    connection = sqlite3.connect(DATABASE_MODELS)
    cursor = connection.cursor()

    # Получение моделей с приоритетами 1 и 2
    cursor.execute("""SELECT name, role, activity, priority FROM models 
    WHERE activity == 'active' AND priority == 2 OR priority == 1
    ORDER BY priority
    """)  # получение данных из таблицы если модель активна
    rows_1_2 = cursor.fetchall()
    rows = rows_1_2
    if priority == 'all':
        cursor.execute("""SELECT name, role, activity, priority FROM models 
        WHERE activity == 'active' AND priority == 3
        ORDER BY name
        """)  # получение данных из таблицы если модель активна
        rows_3 = cursor.fetchall()
        if mixed:
            import random
            rows_3_shuffle = rows_3.copy()
            random.shuffle(rows_3_shuffle)
            rows = rows_1_2 + rows_3_shuffle
        else:  # без сортировки
            rows = rows_1_2 + rows_3

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    cursor.close()

    return rows


DATABASE_CONTENT = read_db(priority='all',  # получение столбцов из БД
                           mixed=True)


def avatar_write_to_db():
    """Функция работы с базой данных"""
    connection = sqlite3.connect(DATABASE_MODELS)
    cursor = connection.cursor()

    cursor.execute("""SELECT name, avatar FROM models
    WHERE activity == 'active'
    ORDER BY name""")
    rows = cursor.fetchall()
    for item in rows:
        if item[1] is None:
            print(f'У модели "{item[0]}" нет аватара!')
            from dictionary_processing import dict_link
            from download_avatars import download_avatars
            from image_path import return_image_path
            download_avatars(verbose=True, dictionary={item[0]: dict_link.get(item[0])})
            file_avatar = return_image_path(model=item[0], avatar=True)
            with open(file_avatar, 'rb') as avatar:
                blob_data = avatar.read()
                sqlite_insert_blob_query = """UPDATE models
                                           SET avatar = ?
                                           WHERE name == ?      
                                           """
                cursor.execute(sqlite_insert_blob_query,
                               [blob_data, item[0]])
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    cursor.close()
    return rows


if __name__ == '__main__':
    import pprint
    # create_db()
    # insert_data_in_table()
    # print(read_db(mixed=True, priority='not all'))
    # print(DATABASE_CONTENT)
    for element in avatar_write_to_db():
        if element[1]:
            print(f"У модели '{element[0]}' есть аватарка в базе данных")
        else:
            print(f"У модели '{element[0]}' нет аватарки в базе данных!")
    # pprint.pprint(avatar_working())
