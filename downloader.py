import os
import subprocess
import time

from write_html import write_html
from links import return_dict_downloads, return_models
from check_parts import searching_parts
from links2 import DICT_LINKS, return_path

COMMAND = "yt-dlp"  # команда для вызова youtube-dl
COMMAND_OPTIONS = (
    '--abort-on-unavailable-fragment',
)

# COMMAND_OPTIONS = (  # параметры youtube-dl
#     "--ignore-config",
#     "--ignore-errors",
#     "--no-warnings",
#     "--console-title",
#     "--fixup", "warn",  # давить попытки "починить" аудио
#     "--force-ipv4",
#     "--socket-timeout", "5"
#     # "--external-downloader", "aria2c",  # не работает на маке, ест много памяти на роутере
#     # "--external-downloader-arg",
#     # "--max-concurrent-downloads=5",
#     # "--max-connection-per-server=5",
#     # "--split=5",
#     # "--min-split-size=1M",
# )


def starting_download():
    """Функция загрузки контента"""
    print("\nНачало загрузки роликов\n".upper())

    for model in return_dict_downloads().keys():
        path = os.path.join(return_dict_downloads().get(model)[0])
        link = return_dict_downloads().get(model)[1]

        if not os.path.isdir(path):
            os.mkdir(path)
        os.chdir(path)

        write_html(path=path, name=model, link=link)

        print(f"Загрузка модели {model.upper()}")
        download_pron = subprocess.call([
            COMMAND,  # распаковка списка с командой youtube-dl
            *COMMAND_OPTIONS,  # параметры youtube-dl, распаковка
            link,  # передаваемая ссылка
        ])

        time.sleep(3)

        while True:
            if searching_parts():
                download_pron = subprocess.call([
                    COMMAND,  # распаковка списка с командой youtube-dl
                    *COMMAND_OPTIONS,  # параметры youtube-dl, распаковка
                    link,  # передаваемая ссылка
                ])
            else:
                break


def starting_download2():
    """Функция загрузки контента"""
    print("\nНачало загрузки роликов\n".upper())

    for model in DICT_LINKS.keys():
        print(model)
        path = DICT_LINKS.get(model)[1]
        link = DICT_LINKS.get(model)[2]
        print(path)
        print(link)
        if not os.path.isdir(path):
            os.mkdir(path)
        os.chdir(path)

        # write_html(path=path, name=model, link=link)
        print(f"Загрузка модели {model.upper()}")
        # input()
        download = subprocess.call([
            COMMAND,  # распаковка списка с командой youtube-dl
            link,  # передаваемая ссылка
            # *COMMAND_OPTIONS,  # параметры youtube-dl, распаковка
        ])

        time.sleep(3)

        while True:
            if searching_parts():
                download_pron = subprocess.call([
                    COMMAND,  # распаковка списка с командой youtube-dl
                    link,  # передаваемая ссылка
                    # *COMMAND_OPTIONS,  # параметры youtube-dl, распаковка
                ])
            else:
                break
