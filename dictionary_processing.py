# Модуль генерации данных для передачи в YOUTUBE-DL или аналоги
# import random
import os
import configparser
from datebase_module import DATABASE_CONTENT

config = configparser.ConfigParser()
config.read('config.ini')
PATH = config.get('SETTINGS',  # получение из конфига пути к каталогу для записи файлов
                  'path')


def return_data():
    """Функция подготовки массивов данных для дальнейшей работы модулей программы"""
    dict_link_ = {}
    dict_path_ = {}
    dict_priority_ = {}
    prioritized_model_shuffle_ = []

    for item in DATABASE_CONTENT:  # перебор кортежей полученных из базы данных
        name_model, type_model, active_model, priority_model = item
        dict_link_.update({name_model:
                          f"https://www.pornhub.com/{type_model}/{name_model}/"})
        dict_path_.update({name_model:
                          f"{PATH}{os.sep}{name_model}"})
        dict_priority_.update({name_model:
                              priority_model})
        prioritized_model_shuffle_.append(item)

    # # Создание списка - массива с моделями
    # for i in dict_priority_.keys():
    #     prioritized_model.append(i)
    # # Создание второго списка для рандомизации значения моделей
    # prioritized_model_shuffle_ = prioritized_model.copy()
    # # TODO очень костыльно реализовал рандомизацию передаваемого списка, надо переделать
    # random.shuffle(prioritized_model_shuffle_)
    # for y in range(1000):  # добавление 1000 пустых элементов в список для будущей рандомизации
    #     prioritized_model_shuffle_.append('')
    #
    # for key, value in dict_priority_.items():
    #     if value == 3:  # по значению приоритета 3 удаляем объект из списка и добавляем в список в случайное место
    #         prioritized_model_shuffle_.remove(key)
    #         prioritized_model_shuffle_.insert(random.randint(100, 999), key)
    #     elif value == 2:  # по аналогии с 3
    #         prioritized_model_shuffle_.remove(key)
    #         prioritized_model_shuffle_.insert(random.randint(50, 99), key)
    #     elif value == 1:  # по аналогии с 3
    #         prioritized_model_shuffle_.remove(key)
    #         prioritized_model_shuffle_.insert(random.randint(0, 49), key)
    #     else:  # если приходит значение вне приоритета от 1 до 3 - ошибка и выход
    #         import sys
    #         sys.exit('Ошибка, нет значения для приоритизации модели')
    #
    # while True:  # удаление пустых строк из списка, созданных ранее
    #     if '' in prioritized_model_shuffle_:
    #         prioritized_model_shuffle_.remove('')
    #     else:
    #         break

    return dict_link_, dict_path_, dict_priority_, prioritized_model_shuffle_


dict_link, dict_path, dict_priority, prioritized_model_shuffle = return_data()


if __name__ == '__main__':
    print(prioritized_model_shuffle)
    print(dict_link)
    print(dict_path)
    print(dict_priority)
