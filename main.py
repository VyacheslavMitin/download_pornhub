#!/opt/bin/python
# Модуль скачки с Порнхаба, в зависимостях aria2c и youtube-dl как отдельная программа в PATH
# "youtube-dl --external-downloader aria2c -i --console-title"

# Импорты
import os
import subprocess
from links import return_dict_downloads, return_models


COMMAND = (  # команда с параметрами youtube-dl
    "youtube-dl",
    "--ignore-errors",
    "--no-warnings",
    # "--external-downloader", "aria2c",
    # "--external-downloader-arg",
    # "--max-concurrent-downloads=5",
    # "--max-connection-per-server=5",
    # "--split=5",
    # "--min-split-size=1M",
)


def starting_download():
    """Функция загрузки контента"""
    print("\nНачало загрузки роликов\n".upper())

    for model in return_dict_downloads().keys():
        path = os.path.join(return_dict_downloads().get(model)[0])
        link = return_dict_downloads().get(model)[1]

        if not os.path.isdir(path):
            os.mkdir(path)
        os.chdir(path)

        download = subprocess.call([
            *COMMAND,  # распаковка списка с командой youtube-dl
            link,  # передаваемая ссылка
        ])


if __name__ == '__main__':
    print("Загрузка роликов с PornHub\n".upper())
    print("Список моделей для скачки:\n".upper(), *return_models(), sep='\n')
    starting_download()
