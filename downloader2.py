import os
import subprocess
import time
import sys

from write_html2 import write_html
from check_parts import searching_parts
from links5 import return_dict_downloads

COMMAND = "yt-dlp"  # команда для вызова youtube-dl или аналогов
COMMAND_OPTIONS = (
    '--abort-on-unavailable-fragment',
    # '--quiet',
    # '--progress'
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

        for i in range(5):
            sys.stdout.write(f"\x1b]2;Загрузка модели {model.upper()}\x07")  # подстановка заголовка в терминал
        print(f"####### Загрузка модели {model.upper()} #######")
        now_time = time.strftime("%d.%m.%Y г. %H:%M:%S")
        download_pron = subprocess.call([
            COMMAND,  # распаковка списка с командой youtube-dl
            *COMMAND_OPTIONS,  # параметры youtube-dl, распаковка
            link,  # передаваемая ссылка
        ])

        time.sleep(1)

        while True:  # Поиск не докаченных файлов
            if searching_parts():
                download_pron = subprocess.call([
                    COMMAND,  # распаковка списка с командой youtube-dl
                    *COMMAND_OPTIONS,  # параметры youtube-dl, распаковка
                    link,  # передаваемая ссылка
                ])
            else:
                break
        # Запись HTML файла с описанием
        write_html(path=path, name=model, link=link, now_time=now_time)

        print(f"####### Окончание загрузки модели {model.upper()} #######" + '\n'*2)
