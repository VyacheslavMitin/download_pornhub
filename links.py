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
NAMES = []

with open(FILE_NAMES, 'r') as file:
    for line in file:  # читать файл построчно
        NAMES.append(line[:-1].lower())  # откусывая перенос строк и в нижнем регистре


# Функции
def return_path(name):
    path = f"{PATH}/{name}"
    path = os.path.join(path)
    return path


def return_link(name):
    link = f"https://www.pornhub.com/model/{name}/videos/upload"
    return link


DICT_LINKS = {}

for item in NAMES:
    DICT_LINKS.update({item: (return_path(item), return_link(item))})


print("Список моделей для скачки:\n", *NAMES, sep='\n')
pprint(DICT_LINKS)
