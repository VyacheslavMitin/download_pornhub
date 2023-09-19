import os
import subprocess
import time

from write_html2 import write_html
from check_parts import searching_parts
from links4 import return_dict_downloads

COMMAND = "yt-dlp"  # команда для вызова youtube-dl или аналогов
COMMAND_OPTIONS = (
    '--abort-on-unavailable-fragment',
    # '--quiet',
    # '--progress'
)


def macos_notifications(title='Title', subtitle='Subtitle'):
    """Функция уведомления в macOS"""
    from functools import partial
    from mac_notifications import client
    if __name__ == "__main__":
        client.create_notification(title=title, subtitle=subtitle)


def starting_download():
    """Функция загрузки контента"""
    print("\nНачало загрузки роликов\n".upper())

    for model in return_dict_downloads().keys():
        path = os.path.join(return_dict_downloads().get(model)[0])
        link = return_dict_downloads().get(model)[1]

        if not os.path.isdir(path):
            os.mkdir(path)
        os.chdir(path)

        print(f"####### Загрузка модели {model.upper()} #######")
        now_time = time.strftime("%d.%m.%Y г. %H:%M:%S")
        download_pron = subprocess.call([
            COMMAND,  # распаковка списка с командой youtube-dl
            *COMMAND_OPTIONS,  # параметры youtube-dl, распаковка
            link,  # передаваемая ссылка
        ])

        time.sleep(1)

        while True:
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
        # Уведомления
        from sys import platform
        if platform == "linux" or platform == "linux2":
            pass  # linux
        elif platform == "darwin":
            macos_notifications(title='Youtube-dl', subtitle=f'{model.upper} загружено')
        elif platform == "win32":
            pass  # Windows...
