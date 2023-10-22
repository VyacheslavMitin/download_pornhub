# Модуль для работы с backend для загрузки
import os
import subprocess
import time
import sys

from write_html import write_html
from check_fragments import searching_unfinished_downloads
from dictionary_processing import dict_link, dict_path, prioritized_model_shuffle
from database_module import avatar_read_from_bd, image_read_from_db, update_attempts
from telegram_notifications import tg_send_notifications
from cookies import COMMAND_OPTIONS_ADD
from disk_usage import disk_free_space

COMMAND = "yt-dlp"  # команда для вызова youtube-dl или аналогов, должна находится в PATH
COMMAND_OPTIONS = [  # параметры для yt-dlp
    '--abort-on-unavailable-fragment',  # отмена загрузки если фрагмент не доступен
    # '--quiet',
    # '--progress'
]

if COMMAND_OPTIONS_ADD:
    COMMAND_OPTIONS = COMMAND_OPTIONS + COMMAND_OPTIONS_ADD

SEPARATOR_START = '🔶' * 5
SEPARATOR_END = '🔷' * 5


def subprocess_download(link_):
    """Функция вызова subprocess с программой-загрузчиком и параметрами"""
    subprocess.call([
        COMMAND,  # распаковка списка с командой youtube-dl
        *COMMAND_OPTIONS,  # параметры youtube-dl, распаковка кортежа с параметрами
        link_,  # передаваемая ссылка на плейлист с каналом модели
    ])
    time.sleep(1)


def starting_download() -> None:
    """Функция загрузки видео контента с PH"""
    print("\n\nНачало загрузки роликов\n\n".upper())
    count = 0

    for model in prioritized_model_shuffle:
        path = dict_path.get(model)
        link = dict_link.get(model)

        # Чтение аватарки из БД
        avatar = avatar_read_from_bd(model)
        # Проверка существования и создания каталога для сохранения загружаемых файлов
        if not os.path.isdir(path):
            try:
                os.mkdir(path)
            except FileNotFoundError as err:
                print(err)
                sys.exit('Нет доступа к каталогу! Выход с ошибкой.')
        os.chdir(path)

        count += 1  # счетчик скачиваемой модели
        progress = f'{count}/{len(prioritized_model_shuffle)}'
        for i in range(5):
            # подстановка заголовка в терминал
            sys.stdout.write(f"\x1b]2;{progress}, модель {model.upper()}\x07")

        attempt = update_attempts(model)
        now_time = time.strftime("%d.%m.%Yг., %H:%M:%S")

        message_start_model_download_print = (f"{SEPARATOR_START} Загрузка {progress},"
                                              f" модель {model.upper()},"
                                              f" попытка {attempt} {SEPARATOR_START}\n"
                                              f"Свободное место - {disk_free_space()}\n")

        message_start_model_download_send = (f"🟢 Началась загрузка {progress}\n"
                                             f"{now_time}\n"
                                             f"Модель {model.upper()}\n"
                                             f"Попытка {attempt}\n"
                                             f"Свободное место - {disk_free_space()}")
        print(message_start_model_download_print)

        tg_send_notifications(captions=message_start_model_download_send, images=avatar)

        searching_unfinished_downloads()  # проверка на фрагменты перед загрузкой

        try:
            while True:
                subprocess_download(link)
                if searching_unfinished_downloads():  # проверка на фрагменты видео,
                    # если есть стереть и перекачать заново
                    continue
                else:
                    break
        except KeyboardInterrupt:  # обработка закрытия программы во время загрузки
            tg_send_notifications(captions=f'🔴 Прерывание работы программы пользователем\n'
                                           f'{time.strftime("%d.%m.%Yг., %H:%M:%S")}',
                                  images=image_read_from_db('interrupt'))

            sys.exit('🔴 Прерывание работы программы пользователем')

        if os.path.isfile('cookies.txt'):  # удаление создаваемых в каталогах моделей куки файлов
            os.remove('cookies.txt')

        # Удаление старого HTML файла
        # from write_html import NAME_HTML
        # if os.path.isfile(NAME_HTML):
        #     os.remove(NAME_HTML)
        # Запись HTML файла с описанием
        write_html(path=path,
                   name=model,
                   link=link,
                   now_time=now_time,
                   attempt=attempt,
                   )
        # Сообщение об окончании загрузки
        message_finish_model_download = (f"\n{SEPARATOR_END} Окончание загрузки модели {model.upper()} {SEPARATOR_END}"
                                         + '\n' * 3)
        print(message_finish_model_download)


if __name__ == '__main__':
    from pprint import pprint
    print(f"Опции для загрузчика {COMMAND_OPTIONS}")
    print()
    print(prioritized_model_shuffle)
    print()
    pprint(dict_link)
    print()
    pprint(dict_path)
