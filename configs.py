# Модуль с конфигурациями
import configparser
import os
import socket

# Получение абсолютного пути к модулю
abs_path = os.path.abspath(os.curdir)
# Чтение конфигурации из файла ini
config = configparser.ConfigParser()
config.read('config.ini')

WEB_SERVER = config.get('SETTINGS',
                        'web_server')


def return_platform() -> str:
    """Функция определения платформы, на которой запускается код"""
    platform = ''
    hostname = socket.gethostname()  # определение через имя хоста
    match hostname:
        case 'Mac-Pro-Vaceslav.local':
            platform = 'mac'
        case 'MacBook-Pro.local':
            platform = 'mac'
        case 'Keenetic_Viva':
            platform = 'wifi_router'
        case 'VYACHESLAV-PC':
            platform = 'win-pc'
    return platform


PLATFORM = return_platform()  # переменная для информации о платформе


def return_paths() -> tuple:
    """Функция возвращения строковых значений путей к каталогам и базе данных"""

    path, database_models = '', ''

    match PLATFORM:
        case 'mac':
            # Путь к каталогу для хранения видео
            path = config.get('SETTINGS',  # получение из конфига пути к каталогу для записи файлов
                              'path_mac')
            # Путь к базе данных
            database_models = config.get('SETTINGS',  # получение из конфига пути к каталогу для записи файлов
                                         'path_database_for_mac')
        case 'wifi_router':
            # Путь к каталогу для хранения видео
            path = config.get('SETTINGS',  # получение из конфига пути к каталогу для записи файлов
                              'path_keenetic_viva')
            # Путь к базе данных
            database_models = os.path.join(abs_path, 'models.db')
        case 'win-pc':
            # Путь к каталогу для хранения видео
            path = config.get('SETTINGS',  # получение из конфига пути к каталогу для записи файлов
                              'path_win')
            # Путь к базе данных
            database_models = config.get('SETTINGS',  # получение из конфига пути к каталогу для записи файлов
                                         'path_database_for_win')

    return path, database_models


PATH, DATABASE_MODELS = return_paths()
# Путь к каталогу для временных файлов в каталоге программы
temp_dir = os.path.join(abs_path, 'tmp/')


if __name__ == '__main__':
    print(WEB_SERVER)
    # print(type(WEB_SERVER))
    print(f"Путь к каталогу для сохранения данных '{PATH}'")
    print(f"Путь к базе данных '{DATABASE_MODELS}'")
    print(f"Путь к каталогу с временными файлами {temp_dir}")
