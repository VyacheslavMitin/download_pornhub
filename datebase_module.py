# Модуль для работы с базами данных
# brew install sqlite
# brew install --cask db-browser-for-sqlite
import sqlite3
import os
import sys

abs_path = os.path.abspath(os.curdir)
DATABASE_MODELS = os.path.join(abs_path, 'models.sq3')


def make_db():
    """Создание таблицы из файла с полями и всем прочим"""
    # Подключаемся к базе и создаем поля
    connection = sqlite3.connect(DATABASE_MODELS)
    cursor = connection.cursor()

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

    models_data = split_models_output()

    def create_db():
        """Функция создания базы данных с моделями"""
        # os.remove(DATABASE_MODELS)
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
        cursor.execute(sqlite_create_table_query)

    def insert_data_in_table():
        """Функция вставки данных в таблицу из специально подготовленного файла"""
        sqlite_inserting_data_in_table_query = '''
        INSERT INTO models (name, role, activity, priority)
        VALUES (?, ?, ?, ?)
        '''

        for item in models_data:
            name, type_model, activ, property_ = item
            cursor.execute(sqlite_inserting_data_in_table_query,
                           [name, type_model, activ, property_])

    split_models_output()
    create_db()
    insert_data_in_table()
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

    if row[1]:  # если есть аватарка в кортеже
        avatar = row[1]
    else:  # если аватарки нет - попытка скачать
        avatar = avatar_update(row[0])
        if avatar is None:
            avatar = image_read_from_db('dummy')  # передача пустышки

    return avatar


def avatar_update(model):
    """Функция обновления аватара в таблице в случае его отсутствия"""
    import shutil
    from download_avatars import download_avatars
    from dictionary_processing import dict_link
    from configs import temp_dir
    model_url = dict_link.get(model)
    # os.makedirs(temp_dir, exist_ok=True)  # создание временного каталога для аватарки
    download_avatars(verbose=False,
                     dictionary={model: model_url})

    path_file = f'{temp_dir}{model}.jpg'
    if os.path.isfile(path_file):  # если аватарка загрузилась - записать ее в БД
        connect = sqlite3.connect(DATABASE_MODELS)
        cur = connect.cursor()
        with open(path_file, 'rb') as avatar:
            blob = avatar.read()
            cur.execute("""UPDATE models
            SET avatar = ?
            WHERE name == ?""", [blob, model])
        connect.commit()
        # прочитать аватарку из БД и передать ее из функции дальше
        cur.execute("""SELECT avatar FROM models
        WHERE name == ?""",
                    [model])
        avatar = cur.fetchone()[0]
        cur.close()
        shutil.rmtree(temp_dir)  # удаление временного каталога для аватарки
        return avatar
    else:
        shutil.rmtree(temp_dir)  # удаление временного каталога для аватарки
        return None


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
    # print(DATABASE_CONTENT)
    # for element in avatar_write_to_db():
    #     if element[1]:
    #         print(f"У модели '{element[0]}' есть аватарка в базе данных")
    #     else:
    #         print(f"У модели '{element[0]}' нет аватарки в базе данных!")
    # pprint.pprint(avatar_working())
    avatar_read_from_bd(model='bubble-lover')
    # avatar_update(model='booty_ass')
    # create_table_images()
    # insert_blob_in_db(table='images', blob='interrupt.jpg', key='interrupt')
    # print(image_read_from_db('interrupt'))
    # import telegram_send
    # telegram_send.send(images=[avatar_read_from_bd(model='booty_ass')],
    #                    captions=['test3'])
    # tuple_ = ('dummy', 'done', 'logo')
    # for item in tuple_:
    #     image_write_to_db(image_=item)
    #     insert_images(file_names=item)
    pass
