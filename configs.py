# Модуль с конфигурациями
import configparser
import os

# Чтение конфигурации из файла ini
config = configparser.ConfigParser()
config.read('config.ini')
PATH = config.get('SETTINGS',  # получение из конфига пути к каталогу для записи файлов
                  'path')


# Путь к базе данных
abs_path = os.path.abspath(os.curdir)
DATABASE_MODELS = os.path.join(abs_path, 'models.db')


# Путь к каталогу для временных файлов в каталоге программы
temp_dir = os.path.join(abs_path, 'tmp/')
