# Модуль для работы с backend для загрузки
import os
import subprocess
import time
import sys
import shutil

from write_html import write_html_model, NAME_HTML_MODEL
from check_fragments import searching_unfinished_downloads
from dictionary_processing import dict_link, dict_path
from database_module import avatar_read_from_bd, image_read_from_db, update_attempts
from telegram_notifications import tg_send_notifications_images, tg_send_notifications_message
from cookies import COMMAND_OPTIONS_ADD
from disk_usage import difference_used_sizes
from configs import WEB_SERVER
from system import update_system_title

COMMAND = "yt-dlp"  # команда для вызова youtube-dl или аналогов, должна находится в PATH
COMMAND_OPTIONS = [  # параметры для yt-dlp
    '--abort-on-unavailable-fragment',  # отмена загрузки если фрагмент не доступен
    # yt-dlp --proxy socks5://proxy.example.com:1080
    # '--proxy', 'socks4://213.74.223.77:4153',
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

    from dictionary_processing import prioritized_model_shuffle
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
        update_system_title(f"{progress}, модель {model.upper()}")

        attempt = update_attempts(model)
        now_time = time.strftime("%d.%m.%Yг., %H:%M:%S")

        message_start_model_download_print = (f"{SEPARATOR_START} Загрузка {progress},"
                                              f" модель {model.upper()},"
                                              f" попытка {attempt} {SEPARATOR_START}\n"
                                              )

        message_start_model_download_send = (f"🟢 Началась загрузка {progress}\n"
                                             f"{now_time}\n"
                                             f"Модель <a href='{WEB_SERVER}/{model}/{NAME_HTML_MODEL}'>{model.upper()}"
                                             f"</a>\n"
                                             # f"Модель {model.upper()}\n"
                                             f"Попытка {attempt}\n"
                                             )
        print(message_start_model_download_print)

        tg_send_notifications_images(captions=message_start_model_download_send,
                                     images=avatar)

        searching_unfinished_downloads()  # проверка на фрагменты перед загрузкой

        try:
            before_size = shutil.disk_usage(path)[2]  # запомнить размер каталога модели до загрузки
        except FileNotFoundError as err:
            print(err)
            before_size = None

        try:
            while True:
                subprocess_download(link)
                if searching_unfinished_downloads():  # проверка на фрагменты видео,
                    # если есть стереть и перекачать заново
                    continue
                else:
                    break
        except KeyboardInterrupt:  # обработка закрытия программы во время загрузки
            tg_send_notifications_images(captions=f'🔴 Прерывание работы программы пользователем\n'
                                                  f'{time.strftime("%d.%m.%Yг., %H:%M:%S")}',
                                         images=image_read_from_db('interrupt'))

            sys.exit('🔴 Прерывание работы программы пользователем')

        if os.path.isfile('cookies.txt'):  # удаление создаваемых в каталогах моделей куки файлов
            os.remove('cookies.txt')

        try:
            after_size = shutil.disk_usage(path)[2]  # запомнить размер каталога модели после загрузки
        except FileNotFoundError as err:
            print(err)
            print(f"Не удалось высчитать размер загруженных файлов по модели {model.upper}")
            tg_send_notifications_message(f"Не удалось высчитать размер загруженных файлов по модели {model.upper}")
        else:
            if before_size is not None:
                difference_size = difference_used_sizes(before_size, after_size)
                message_finish_model_download = (
                            f"\n{SEPARATOR_END} Окончание загрузки модели {model.upper()} {SEPARATOR_END}"
                            + f"\nЗагружено {difference_size}" + '\n' * 3)
                print(message_finish_model_download)

                if difference_size != '0.00 Б':
                    tg_send_notifications_message(f"Загружено: {difference_size}")
            else:
                print(f"Не удалось высчитать размер загруженных файлов по модели {model.upper}")
                tg_send_notifications_message(f"Не удалось высчитать размер загруженных файлов по модели {model.upper}")

        # Запись HTML файла с описанием
        write_html_model(path=path,
                         name=model,
                         link=link,
                         now_time=now_time,
                         attempt=attempt,
                         )
        # Сообщение об окончании загрузки


if __name__ == '__main__':
    from pprint import pprint

    print(f"Опции для загрузчика {COMMAND_OPTIONS}")
    print()
    # print(prioritized_model_shuffle)
    print()
    pprint(dict_link)
    print()
    pprint(dict_path)
