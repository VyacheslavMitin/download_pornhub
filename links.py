# Модуль для генерации путей и ссылок

import os
import configparser

# Константы
config = configparser.ConfigParser()
config.read('config.ini')
PATH = config.get('SETTINGS', 'path')  # получение из конфига пути к каталогу для записи файлов


def return_path(name) -> str:
    """Функция возврата пути папки для загрузки"""
    path = f"{PATH}{os.sep}{name}"  # путь вида '/Users/sonic/PycharmProjects/download_pornhub/test/wettmelons'
    path = os.path.join(path)  # превращение пути в формат для путей
    return path


def return_dict_downloads(sorting='mix') -> dict:
    """Функция возврата данных для загрузки.

    Здесь создаются ссылки для передачи в программу для скачивания видео"""
    dict_links = {}
    from models_list import union_models, PORNSTARS
    list_ = []
    match sorting:
        case 'sort':
            list_ = union_models('sorted')
        case 'mix':
            list_ = union_models('mixed')

    for item in list_:
        if item not in PORNSTARS:
            dict_links.update({item: (return_path(item), f"https://www.pornhub.com/model/{item}/")})
        else:
            dict_links.update({item: (return_path(item), f"https://www.pornhub.com/pornstar/{item}/")})
    return dict_links


RETURN_DICT_DOWNLOADS = return_dict_downloads(sorting='mix')


def return_models() -> list:
    """Функция формирования имен моделей для загрузки"""
    names = []
    for name in RETURN_DICT_DOWNLOADS.keys():
        names.append(name)
    return names


RETURN_MODELS = return_models()


if __name__ == '__main__':
    from pprint import pprint
    pprint(RETURN_MODELS)
    pprint(return_dict_downloads())
