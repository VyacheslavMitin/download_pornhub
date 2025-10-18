# Модуль для работы с базами данных
# brew install sqlite
# brew install --cask db-browser-for-sqlite
import sqlite3
import os
import sys

from configs import DATABASE_MODELS, DATABASE_MODELS_TEST
# TODO сделать общую точка входа в базу данных


def make_db():
    """Создание таблицы из файла с полями и всем прочим"""
    # Подключаемся к базе и создаем поля
    connect = sqlite3.connect(DATABASE_MODELS)
    cursor = connect.cursor()

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
        attempts INTEGER DEFAULT 0,
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
    connect.commit()
    cursor.close()


def read_db(priority='all',  # not_all
            mixed=True):
    """Функция чтения данных из базы данных"""
    connect = sqlite3.connect(DATABASE_MODELS)
    cursor = connect.cursor()
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

    cursor.close()

    return rows


DATABASE_CONTENT = read_db(priority='all',  # получение столбцов из БД
                           mixed=True)


def insert_new_model(name=None, role='model', priority=1):
    """Функция вставки новой модели в базу данных перед загрузкой"""
    connect = sqlite3.connect(DATABASE_MODELS)
    cursor = connect.cursor()

    if name is None:  # запрос на ввод данных если они не передаются в параметрах функции
        print("Необходимо ввести данные по новой модели\n")
        while True:
            name = input("Имя модели: ")
            if not name:  # проверка на пустой ввод
                print("Имя не корректно, ввести заново")
            if name:
                break
        while True:  # получение от пользователя строки с типом модели
            role_tuple = ('model', 'pornstar',)
            role = input("Это 'model' или 'pornstar' (по умолчанию model):  ").lower()
            if role not in role_tuple and role != '':
                print(f'Необходимо ввести правильную роль из {role_tuple}!')
            elif role == '':
                role = 'model'
                break
            else:
                break

        while True:  # получение от пользователя числа с приоритетом для порядка
            priority_tuple = ('1', '2', '3',)
            priority = input("Приоритет 1, 2 или 3 (по умолчанию 1):  ")
            if priority not in priority_tuple and priority != '':
                print(f'Необходимо указать корректный порядок - из {priority_tuple}')
            elif priority == '':
                priority = 1
                break
            else:
                priority = int(priority)
                break

    try:
        cursor.execute("""INSERT INTO models (name, role, priority)
        VALUES (?, ?, ?)""",
                       [name, role, priority])
    except sqlite3.IntegrityError:
        print("Модель уже есть в базе данных")
    finally:
        connect.commit()
        cursor.close()

    # global DATABASE_CONTENT
    # DATABASE_CONTENT = read_db(priority='all',  # получение столбцов из БД
    #                            mixed=True)


def avatar_read_from_bd(model):
    """Функция чтения аватарок или их замены из базы данных"""
    connect = sqlite3.connect(DATABASE_MODELS)
    cursor = connect.cursor()

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
    # import shutil
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
        cursor = connect.cursor()
        with open(path_file, 'rb') as avatar:
            blob = avatar.read()
            cursor.execute("""UPDATE models
            SET avatar = ?
            WHERE name == ?""", [blob, model])
        connect.commit()
        # прочитать аватарку из БД и передать ее из функции дальше
        cursor.execute("""SELECT avatar FROM models
        WHERE name == ?""",
                       [model])
        avatar = cursor.fetchone()[0]
        cursor.close()
        # shutil.rmtree(temp_dir)  # удаление временного каталога для аватарки
        return avatar
    else:
        # shutil.rmtree(temp_dir)  # удаление временного каталога для аватарки
        return None


def image_read_from_db(file_name):
    """Функция чтения картинок (не аватарок) из базы данных"""
    connect = sqlite3.connect(DATABASE_MODELS)
    cursor = connect.cursor()

    cursor.execute("""SELECT image FROM images
    WHERE file_name == ?""",
                   [file_name])

    image = cursor.fetchone()[0]

    # Закрываем соединение
    connect.close()

    return image


def insert_blob(table, blob, key):
    """Функция записи файлов в базу данных"""
    if os.path.isfile(blob):
        connect = sqlite3.connect(DATABASE_MODELS)
        cursor = connect.cursor()

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
    connect.commit()
    connect.close()


def update_attempts(model):
    """Функция для обновления количества попыток загрузки"""
    connect = sqlite3.connect(DATABASE_MODELS)
    cursor = connect.cursor()

    sql_query_select_attempts = """SELECT attempts FROM models WHERE name = ?"""
    cursor.execute(sql_query_select_attempts, [model])
    attempt = cursor.fetchone()[0]
    attempt = attempt + 1
    sql_query_update_attempts = """UPDATE models
    SET attempts = ?
    where name == ?"""

    cursor.execute(sql_query_update_attempts, [attempt, model])

    connect.commit()
    cursor.close()

    return attempt


def view_db(mode='active'):
    """Функция чтения данных из базы данных в человеко читаемом виде"""
    connect = sqlite3.connect(DATABASE_MODELS)
    cursor = connect.cursor()
    sql_query = """SELECT name, role, activity, priority, attempts FROM models 
    WHERE activity == 'active'
    ORDER BY name
    """
    if mode == 'active':
        print("Только активные модели в БД")
    elif mode == 'all':
        print("Все модели в БД")
        sql_query =  """SELECT name, role, activity, priority, attempts FROM models 
    ORDER BY name
    """
    cursor.execute(sql_query)  # получение данных из таблицы если модель активна
    rows_ = [('ИМЯ', 'ТИП', 'АКТИВНОСТЬ', 'ПРИОРИТЕТ', 'ПОПЫТКИ')] + cursor.fetchall()

    for item in rows_:
        print("{:<20}{:<10}{:<12}{:<10}{:<10}".format(*item))


def delete_model():
    """Функция удаление моделей"""
    connect = sqlite3.connect(DATABASE_MODELS)
    cursor = connect.cursor()

    view_db(mode='all')
    model = input("\nВведите имя модели для удаления: ")

    try:
        cursor.execute("""DELETE FROM models WHERE name = ?""", [model])
    except sqlite3.Error:
        print("Не правильное имя модели")
    else:
        print(f"Модель '{model.upper()}' из БД удалена")

    connect.commit()
    cursor.close()


def update_model():
    """Функция включения и отключения моделей в БД"""
    connect = sqlite3.connect(DATABASE_MODELS)
    cursor = connect.cursor()

    view_db(mode='all')
    work = 'foobar'
    column = 'foobar'

    model = input("\nВведите имя модели для обработки: ")
    mode = input("Введите режим работы\n"
                 "1 - Включение\n"
                 "2 - Выключение\n"
                 "3 - Новое имя\n"
                 "4 - Приоритет\n"
                 "ВВОД: ")
    if mode == '1':
        print("Включение модели")
        column = 'activity'
        work = 'active'
    elif mode == '2':
        print("Выключение модели")
        column = 'activity'
        work = 'not_active'
    elif mode == '3':
        new_name = input("Новое имя для модели\nВВОД: ")
        column = 'name'
        work = new_name
    elif mode == '4':
        new_priority = input("Приоритет 1, 2 или 3\nВВОД: ")
        column = 'priority'
        work = new_priority

    try:
        sql_query_update_activity = f"""UPDATE models
        SET {column} = ?
        where name == ?"""

        cursor.execute(sql_query_update_activity, [work, model])
    except sqlite3.Error:
        print("Не правильное имя модели")
    else:
        print(f"Модель '{model.upper()}' в БД обработана - '{column}'")

    connect.commit()
    cursor.close()


def db_menu():
    """Функция режима выбора меню работы с БД"""
    while True:
        menu = input(
"""Выбрать режим работы с базой данных

    0 - Вывод всей БД
    1 - Вывод активных моделей в БД
    2 - Добавить модель в БД
    3 - Обновление модели в БД
    4 - Удаление модели в БД


ВВОД: """
        )
        if menu == "0":
            print('Содержимое БД (полное)\n')
            view_db(mode='all')
            print('\n')
        elif menu == "1":
            print('Содержимое БД\n')
            view_db()
            print('\n')
        elif menu == "2":
            print("Ввод новой модели\n")
            insert_new_model()
            print('\n')
        elif menu == "3":
            print("Обновление модели\n")
            update_model()
            print('\n')
        elif menu == "4":
            print("Удаление модели\n")
            delete_model()
            print('\n')
        else:
            print("Не выбрано корректное меню, выход\n")
            sys.exit()


if __name__ == '__main__':
    from system import check_all
    check_all()
    print("Работа с базой данных для модуля DownloadPH")
    from main import __version__
    print(f"Версия программы {__version__}\n")
    db_menu()
