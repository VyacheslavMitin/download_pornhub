# Модуль генерации путей и ссылок

# Импорты
import os
import configparser

# Константы
config = configparser.ConfigParser()
config.read('config.ini')
PATH = config.get('SETTINGS', 'path')
# Массивы данных для будущей работы
DICT_LINKS = {}


# Функции
def return_path(name) -> str:
    """Функция возврата пути папки для загрузки"""
    path = f"{PATH}{os.sep}{name}"  # путь вида '/Users/sonic/PycharmProjects/download_pornhub/test/wettmelons'
    path = os.path.join(path)  # превращение пути в формат для путей
    return path


def return_dict_downloads(sorting='mix') -> dict:
    """Функция возврата данных для загрузки.

    Здесь создаются ссылки для передачи в программу для скачивания видео"""
    from models_list import union_models, PORNSTARS
    list_ = []
    match sorting:
        case 'sort':
            list_ = union_models('sorted')
        case 'mix':
            list_ = union_models('mixed')

    for item in list_:
        if item not in PORNSTARS:
            DICT_LINKS.update({item: (return_path(item), f"https://www.pornhub.com/model/{item}/")})
        else:
            DICT_LINKS.update({item: (return_path(item), f"https://www.pornhub.com/pornstar/{item}/")})
    return DICT_LINKS


def return_models() -> list:
    """Функция формирования имен моделей для загрузки"""
    names = []
    for name in return_dict_downloads().keys():
        names.append(name)
    return names


if __name__ == '__main__':
    from pprint import pprint
    pprint(return_models())
    pprint(return_dict_downloads())
