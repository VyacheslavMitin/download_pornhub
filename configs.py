# Модуль с конфигурациями
import configparser
import os
import socket
import datetime

# Получение абсолютного пути к модулю
abs_path = os.path.abspath(os.curdir)
# Чтение конфигурации из файла ini
config = configparser.ConfigParser()
config.read('config.ini')

SYS_DIR = config.get('SETTINGS',
                    'sys_dir')

MODELS_DB = config.get('SETTINGS',
                    'models')

MODELS_TEST_DB = config.get('SETTINGS',
                    'models_test')

WEB_SERVER = config.get('SETTINGS',
                        'web_server')


def return_platform() -> str:
    """Функция определения платформы, на которой запускается код"""
    platform = ''
    hostname = socket.gethostname()  # определение через имя хоста
    match hostname:
        case s if s.startswith('Mac-'):
            platform = 'mac'
        case s if s.startswith('MacBook-'):
            platform = 'mac'
        case s if s.startswith('Keenetic_'):
            platform = 'wifi_router'
        case s if s.startswith('Netcraze_'):
            platform = 'wifi_router'
        case s if s.endswith('-PC'):
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
            # database_models = config.get('SETTINGS',  # получение из конфига пути к каталогу для записи файлов
            #                              'path_database_for_mac')
            database_models = f'{path}{os.sep}{SYS_DIR}{os.sep}{MODELS_DB}'
            database_models_test = f'{path}{os.sep}{SYS_DIR}{os.sep}{MODELS_TEST_DB}'
        case 'wifi_router':
            # Путь к каталогу для хранения видео
            path = config.get('SETTINGS',  # получение из конфига пути к каталогу для записи файлов
                              'path_keenetic')
            # Путь к базе данных
            database_models = f'{path}{os.sep}{SYS_DIR}{os.sep}{MODELS_DB}'
            database_models_test = f'{path}{os.sep}{SYS_DIR}{os.sep}{MODELS_TEST_DB}'
        case 'win-pc':
            # Путь к каталогу для хранения видео
            path = config.get('SETTINGS',  # получение из конфига пути к каталогу для записи файлов
                              'path_win')
            # Путь к базе данных
            # TODO переделать путь по винде
            database_models = config.get('SETTINGS',  # получение из конфига пути к каталогу для записи файлов
                                         'path_database_for_win')

    return path, database_models, database_models_test


PATH, DATABASE_MODELS, DATABASE_MODELS_TEST = return_paths()
# Путь к каталогу для временных файлов в каталоге программы, пока не используется
temp_dir = os.path.join(abs_path, 'tmp/')

# Для работы с дублями
current_datetime = datetime.datetime.now()
formatted_date = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
doubles_log_dir = os.path.join(abs_path, 'doubles/')  # путь к каталогу куда кладутся логи дублей
# doubles_log_dir = temp_dir
doubles_log_file = f'{doubles_log_dir}{formatted_date}.txt'

if __name__ == '__main__':
    print(f"Путь к каталогу с системными файлами: '{SYS_DIR}'")
    print(f"Веб сервер: '{WEB_SERVER}'")
    print(f"Платформа: '{PLATFORM}'")
    print(f"Путь к каталогу для сохранения данных '{PATH}'")
    print(f"Путь к базе данных '{DATABASE_MODELS}'")
    print(f"Путь к каталогу с временными файлами '{temp_dir}'")
    print(f"Лог файл с дублями файлов '{doubles_log_file}'")
