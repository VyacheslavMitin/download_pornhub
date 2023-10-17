# Модуль генерации данных для передачи в YOUTUBE-DL или аналоги
import os

from configs import PATH
from datebase_module import DATABASE_CONTENT


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
        prioritized_model_shuffle_.append(name_model)

    return dict_link_, dict_path_, dict_priority_, prioritized_model_shuffle_


dict_link, dict_path, dict_priority, prioritized_model_shuffle = return_data()


if __name__ == '__main__':
    print(prioritized_model_shuffle)
    print(dict_link)
    print(dict_path)
    print(dict_priority)
