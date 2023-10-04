# Модуль для работы с backend для загрузки
import os
import subprocess
import time
import sys

from write_html2 import write_html
from check_fragments import searching_parts
from links import return_dict_downloads

COMMAND = "yt-dlp"  # команда для вызова youtube-dl или аналогов
COMMAND_OPTIONS = (
    '--abort-on-unavailable-fragment',
    # '--quiet',
    # '--progress'
)
SEPARATOR = '#######'

def starting_download():
    """Функция загрузки контента"""
    print("\nНачало загрузки роликов\n".upper())

    for model in return_dict_downloads().keys():
        path = os.path.join(return_dict_downloads().get(model)[0])
        link = return_dict_downloads().get(model)[1]

        if not os.path.isdir(path):
            try:
                os.mkdir(path)
            except FileNotFoundError as err:
                print(err)
                sys.exit('Нет доступа к каталогу! Выход с ошибкой.')
        os.chdir(path)

        for i in range(5):
            sys.stdout.write(f"\x1b]2;Загрузка модели {model.upper()}\x07")  # подстановка заголовка в терминал
        print(f"{SEPARATOR} Загрузка модели {model.upper()} {SEPARATOR}\n")
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

        print(f"{SEPARATOR} Окончание загрузки модели {model.upper()} {SEPARATOR}" + '\n'*10)
