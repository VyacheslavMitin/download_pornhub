# Модуль с конфигурациями
import configparser
import os
import sys
import socket

# Получение абсолютного пути к модулю
abs_path = os.path.abspath(os.curdir)
# Чтение конфигурации из файла ini
config = configparser.ConfigParser()
config.read('config.ini')


def return_platform() -> str:
    """Функция определения платформы, на которой запускается код"""
    platform = ''
    hostname = socket.gethostname()  # определение через имя хоста
    match hostname:
        case 'MacBook-Pro-Vaceslav.local':
            platform = 'macbook'
        case 'Keenetic_Viva':
            platform = 'wifi_router'
    return platform


PLATFORM = return_platform()  # переменная для информации о платформе


def return_paths() -> tuple:
    """Функция возвращения строковых значений путей к каталогам и базе данных"""

    path, database_models = '', ''

    match PLATFORM:
        case 'macbook':
            # Путь к каталогу для хранения видео
            path = config.get('SETTINGS',  # получение из конфига пути к каталогу для записи файлов
                              'path_macbook')
            # Путь к базе данных
            database_models = config.get('SETTINGS',  # получение из конфига пути к каталогу для записи файлов
                                         'path_database_for_macbook')
        case 'wifi_router':
            # Путь к каталогу для хранения видео
            path = config.get('SETTINGS',  # получение из конфига пути к каталогу для записи файлов
                              'path_keenetic_viva')
            # Путь к базе данных
            database_models = os.path.join(abs_path, 'models.db')

    return path, database_models


PATH, DATABASE_MODELS = return_paths()
# Путь к каталогу для временных файлов в каталоге программы
temp_dir = os.path.join(abs_path, 'tmp/')


if __name__ == '__main__':
    print(f"Путь к каталогу для сохранения данных '{PATH}'")
    print(f"Путь к базе данных '{DATABASE_MODELS}'")
    print(f"Путь к каталогу с временными файлами {temp_dir}")
