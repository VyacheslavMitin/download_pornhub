# Модуль для работы с backend для загрузки
import os
import subprocess
import time
import sys

import telegram_send

from write_html import write_html
from check_fragments import searching_parts
from links import RETURN_DICT_DOWNLOADS

COMMAND = "yt-dlp"  # команда для вызова youtube-dl или аналогов
COMMAND_OPTIONS = (
    '--abort-on-unavailable-fragment',
    # '--quiet',
    # '--progress'
)
SEPARATOR = '~' * 8


def starting_download():
    """Функция загрузки контента"""
    print("\n\n\nНачало загрузки роликов\n\n\n".upper())
    count = 0
    for model in RETURN_DICT_DOWNLOADS.keys():
        path = os.path.join(RETURN_DICT_DOWNLOADS.get(model)[0])
        link = RETURN_DICT_DOWNLOADS.get(model)[1]

        if not os.path.isdir(path):
            try:
                os.mkdir(path)
            except FileNotFoundError as err:
                print(err)
                sys.exit('Нет доступа к каталогу! Выход с ошибкой.')
        os.chdir(path)

        count += 1  # счетчик скачиваемой модели
        progress = f'{count}/{len(RETURN_DICT_DOWNLOADS.keys())}'
        for i in range(5):
            sys.stdout.write(f"\x1b]2;Загрузка {progress}, модель {model.upper()}\x07")  # подстановка заголовка в терминал

        print(f"{SEPARATOR} Загрузка {progress}, модель {model.upper()} {SEPARATOR}\n")
        now_time = time.strftime("%d.%m.%Yг., %H:%M:%S")
        subprocess.call([
            COMMAND,  # распаковка списка с командой youtube-dl
            *COMMAND_OPTIONS,  # параметры youtube-dl, распаковка
            link,  # передаваемая ссылка
        ])

        time.sleep(1)

        while True:  # Поиск не докаченных файлов
            if searching_parts():
                subprocess.call([
                    COMMAND,  # распаковка списка с командой youtube-dl
                    *COMMAND_OPTIONS,  # параметры youtube-dl, распаковка
                    link,  # передаваемая ссылка
                ])
            else:
                break
        # Запись HTML файла с описанием
        write_html(path=path,
                   name=model,
                   link=link,
                   now_time=now_time
                   )

        print(f"\n{SEPARATOR} Окончание загрузки модели {model.upper()} {SEPARATOR}" + '\n'*10)
