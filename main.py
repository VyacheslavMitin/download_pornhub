#!/opt/bin/python
# Модуль скачки с Порнхаба, в зависимостях aria2c и youtube-dl как отдельная программа в PATH
# "youtube-dl --external-downloader aria2c -i --console-title"

# Импорты
from links3 import return_models
from downloader import starting_download


if __name__ == '__main__':
    print("Загрузка роликов с PornHub\n".upper())
    print("Список моделей для скачки:\n".upper(), *return_models(), sep='\n')
    starting_download()
