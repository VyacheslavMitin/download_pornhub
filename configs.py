# Модуль с конфигурациями
import configparser
import os


from datebase_module import abs_path

config = configparser.ConfigParser()
config.read('config.ini')
PATH = config.get('SETTINGS',  # получение из конфига пути к каталогу для записи файлов
                  'path')


temp_dir = os.path.join(abs_path, 'tmp/')
