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

WEB_SERVER = config.get('SETTINGS',
                        'web_server')


def return_platform() -> str:
    """Функция определения платформы, на которой запускается код"""
    platform = ''
    hostname = socket.gethostname()  # определение через имя хоста
    match hostname:
        case s if s.startswith('Mac-'):
            platform = 'mac'
            # print('mac')
        # case 'Mac-Pro-Vaceslav.local':
        #     platform = 'mac'
        # case 'MacBook-Pro.local':
        #     platform = 'mac'
        # case 'Mac-mini-Vaceslav.local':
        #     platform = 'mac'
        # case 'Mac-mini-M4.local':
        #     platform = 'mac'
        case s if s.startswith('Keenetic_'):
            platform = 'wifi_router'
        # case 'Keenetic_Viva':
        #     platform = 'wifi_router'
        # case 'Keenetic_Ultra':
        #     platform = 'wifi_router'
        case s if s.endswitch('-PC'):
            platform = 'win-pc'
        # case 'VYACHESLAV-PC':
        #     platform = 'win-pc'
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
                              'path_keenetic')
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
# Путь к каталогу для временных файлов в каталоге программы, пока не используется
temp_dir = os.path.join(abs_path, 'tmp/')

# Для работы с дублями
current_datetime = datetime.datetime.now()
formatted_date = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
doubles_log_dir = os.path.join(abs_path, 'doubles/')  # путь к каталогу куда кладутся логи дублей
doubles_log_file = f'{doubles_log_dir}{formatted_date}.txt'

if __name__ == '__main__':
    print(WEB_SERVER)
    # print(type(WEB_SERVER))
    print(f"Путь к каталогу для сохранения данных '{PATH}'")
    print(f"Путь к базе данных '{DATABASE_MODELS}'")
    print(f"Путь к каталогу с временными файлами '{temp_dir}'")
    print(f"Платформа: '{PLATFORM}'")
    print(f"Лог файл с дублями файлов '{doubles_log_file}'")
