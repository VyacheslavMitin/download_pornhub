# Модуль генерации путей и ссылок

# Импорты
import os
import configparser
from pprint import pprint

# Константы
config = configparser.ConfigParser()
config.read('config.ini')
PATH = config.get('SETTINGS', 'path')
FILE_NAMES = config.get('SETTINGS', 'file_names')
# Массивы данных для будущей работы
NAMES = []
DICT_LINKS = {}


# Функции
def return_models() -> list:
    """Функция формирования имен моделей для загрузки"""
    with open(FILE_NAMES, 'r') as file:
        for line in file:  # читать файл построчно
            if line[0] != '#':  # если строка не закомментирована
                NAMES.append(line[:-1].lower())  # откусывая перенос строк и в нижнем регистре
    return NAMES


def return_path(name) -> str:
    """Функция возврата пути папки для загрузки"""
    path = f"{PATH}/{name}"  # путь вида '/Users/sonic/PycharmProjects/download_pornhub/test/wettmelons'
    path = os.path.join(path)  # превращение пути в формат для путей
    return path


def return_link(name) -> str:
    """Функция возврата ссылки для загрузки"""
    link = f"https://www.pornhub.com/model/{name}/videos/upload"
    return link


def return_dict_downloads() -> dict:
    """Функция возврата данных для загрузки"""
    for item in return_models():
        DICT_LINKS.update({item: (return_path(item), return_link(item))})
    return DICT_LINKS


if __name__ == '__main__':
    pprint(return_dict_downloads())
