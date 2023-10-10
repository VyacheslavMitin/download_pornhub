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
    models = []
    match sorting:
        case 'sort':
            models = union_models('sorted')
        case 'mix':
            models = union_models('mixed')

    for model in models:
        if model not in PORNSTARS:
            # Формирование словаря с именем модели, путями, и ссылкой на страничку модели
            # Словарь вида {МОДЕЛЬ: [ПУТЬ К КАТАЛОГУ, ССЫЛКА НА ПОРНХАБ]}, то есть значение это список
            dict_links.update({model:
                              (return_path(model),
                               f"https://www.pornhub.com/model/{model}/")})
        else:
            dict_links.update({model:
                              (return_path(model),
                               f"https://www.pornhub.com/pornstar/{model}/")})
    return dict_links


RETURN_DICT_DOWNLOADS = return_dict_downloads(sorting='mix')


def return_models() -> list:
    """Функция формирования имен моделей для загрузки"""
    names = []
    for name in RETURN_DICT_DOWNLOADS.keys():
        names.append(name)
    return names


RETURN_MODELS = return_models()  # повторяемый лист обработки в main.py

if __name__ == '__main__':
    from pprint import pprint
    pprint(RETURN_MODELS)
    pprint(return_dict_downloads())
