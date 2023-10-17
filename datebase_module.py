# Модуль для работы с базами данных
# brew install sqlite
# brew install --cask db-browser-for-sqlite
import sqlite3
import os
import sys

abs_path = os.path.abspath(os.curdir)
DATABASE_MODELS = os.path.join(abs_path, 'models.sq3')


def split_models_output():
    """Функция для нарезания файла с моделями в список"""
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
    # os.remove(DATABASE_MODELS)

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
    """Функция чтения данных из базы данных"""
    connection = sqlite3.connect(DATABASE_MODELS)
    cursor = connection.cursor()

    # Получение моделей с приоритетами 1 и 2
    cursor.execute("""SELECT name, role, activity, priority FROM models 
    WHERE activity == 'active' AND (priority == 2 OR priority == 1)
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
    """Функция записи аватарок в базу данных"""
    connection = sqlite3.connect(DATABASE_MODELS)
    cursor = connection.cursor()

    cursor.execute("""SELECT name, avatar FROM models
    WHERE activity == 'active'
    ORDER BY name
    """)  # получение строк в БД для проверки существования аватарок
    rows = cursor.fetchall()
    for item in rows:
        if item[1] is None:  # если нет аватара попробовать его загрузить и записать в БД
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
                cursor.execute(sqlite_insert_blob_query,  # обновление БД с записью в нее загруженных аватарок
                               [blob_data, item[0]])
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    cursor.close()
    return rows


def avatar_read_from_bd(model):
    """Функция чтения аватарок или их замены из базы данных"""
    connection = sqlite3.connect(DATABASE_MODELS)
    cursor = connection.cursor()

    cursor.execute("""SELECT name, avatar FROM models
    WHERE name == ?
    """, [model])

    row = cursor.fetchone()

    # Закрываем соединение
    cursor.close()

    if row[1]:  # если есть аватар в кортеже
        avatar = row[1]
    else:
        avatar = image_read_from_db('dummy')  # передача пустышки

    return avatar


def image_read_from_db(file_name):
    """Функция чтения картинок (не аватарок) из базы данных"""
    conn = sqlite3.connect(DATABASE_MODELS)
    cursor = conn.cursor()

    cursor.execute("""SELECT image FROM images
    WHERE file_name == ?""",
                   [file_name])

    image = cursor.fetchone()[0]

    # Закрываем соединение
    conn.close()

    return image


def insert_blob_in_db(table, blob, key):
    """Функция записи файлов в базу данных"""
    conn = sqlite3.connect(DATABASE_MODELS)
    cursor = conn.cursor()

    if os.path.isfile(blob):
        blob_data = open(blob, 'rb')
        blob_data_read = blob_data.read()

        cursor.execute(f"""UPDATE {table}
        SET image = ?
        WHERE file_name == ?""",
                       [blob_data_read, key])
        # Закрываем файл
        blob_data.close()
    else:
        sys.exit('Нет файла для записи в базу данных')
    # Закрываем соединение с БД с сохранением данных
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # import pprint
    # create_db()
    # insert_data_in_table()
    # print(read_db(mixed=True, priority='not all'))
    print(DATABASE_CONTENT)
    # for element in avatar_write_to_db():
    #     if element[1]:
    #         print(f"У модели '{element[0]}' есть аватарка в базе данных")
    #     else:
    #         print(f"У модели '{element[0]}' нет аватарки в базе данных!")
    # pprint.pprint(avatar_working())
    # avatar_read_from_bd(model='booty_ass')
    # create_table_images()
    insert_blob_in_db(table='images', blob='interrupt.jpg', key='interrupt')
    print(image_read_from_db('interrupt'))
    # import telegram_send
    # telegram_send.send(images=[avatar_read_from_bd(model='booty_ass')],
    #                    captions=['test3'])
    # tuple_ = ('dummy', 'done', 'logo')
    # for item in tuple_:
    #     image_write_to_db(image_=item)
    #     insert_images(file_names=item)
    pass
