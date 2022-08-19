# Модуль генерации путей и ссылок

# Импорты
import os
import random
import configparser
from pprint import pprint
from models_list import MODELS, PORNSTARS

# Константы
config = configparser.ConfigParser()
config.read('config.ini')
PATH = config.get('SETTINGS', 'path')
# FILE_NAMES = config.get('SETTINGS', 'file_names')
# Массивы данных для будущей работы
NAMES = []
DICT_LINKS = {}


# Функции
def return_path(name) -> str:
    """Функция возврата пути папки для загрузки"""
    path = f"{PATH}/{name}"  # путь вида '/Users/sonic/PycharmProjects/download_pornhub/test/wettmelons'
    path = os.path.join(path)  # превращение пути в формат для путей
    return path


# def return_link(name) -> str:
#     """Функция возврата ссылки для загрузки"""
#
#     # link = f"https://www.pornhub.com/pornstar/{name}/"
#     # link = f"https://www.pornhub.com/pornstar/{name}/videos/"
#     # link = f"https://www.pornhub.com/pornstar/{name}/videos/upload/"
#     # link = f"https://www.pornhub.com/pornstar/{name}/public/videos/"
#
#     link = f"https://www.pornhub.com/model/{name}/"
#     # link = f"https://www.pornhub.com/model/{name}/videos/upload/"
#     # link = f"https://www.pornhub.com/model/{name}/videos/"
#     # link = f"https://www.pornhub.com/model/{name}/public/videos/"
#
#     return link


def return_dict_downloads() -> dict:
    """Функция возврата данных для загрузки"""
    for item in MODELS:
        DICT_LINKS.update({item: (return_path(item), f"https://www.pornhub.com/model/{item}/")})
    for item in PORNSTARS:
        DICT_LINKS.update({item: (return_path(item), f"https://www.pornhub.com/pornstar/{item}/")})
    return DICT_LINKS


def return_models() -> list:
    """Функция формирования имен моделей для загрузки"""
    names = []
    for name in return_dict_downloads().keys():
        names.append(name)
    return names


if __name__ == '__main__':
    pprint(return_models())
    pprint(return_dict_downloads())
