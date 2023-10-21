# Модуль для работы с backend для загрузки
import os
import subprocess
import time
import sys

import telegram_send

from write_html import write_html
from check_fragments import searching_parts
from dictionary_processing import dict_link, dict_path, prioritized_model_shuffle
from database_module import avatar_read_from_bd, image_read_from_db, update_attempts

COMMAND = "yt-dlp"  # команда для вызова youtube-dl или аналогов, должна находится в PATH
COMMAND_OPTIONS = (
    '--abort-on-unavailable-fragment',
    # '--quiet',
    # '--progress'
)
SEPARATOR = '~' * 8


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

        # Путь к файлу с аватаркой модели
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
            sys.stdout.write(f"\x1b]2;Загрузка {progress}, модель {model.upper()}\x07")

        attempt = update_attempts(model)
        now_time = time.strftime("%d.%m.%Yг., %H:%M:%S")

        message_start_model_download_print = (f"{SEPARATOR} Загрузка {progress},"
                                              f" модель {model.upper()},"
                                              f" попытка {attempt} {SEPARATOR}\n")

        message_start_model_download_send = (f"🟢Началась загрузка {progress}\n"
                                             f"{now_time}\n"
                                             f"Модель {model.upper()}\n"
                                             f"Попытка {attempt}")
        print(message_start_model_download_print)

        try:
            telegram_send.send(
                images=[avatar],
                captions=[message_start_model_download_send],
            )
        except:
            print('Не удалось отправить уведомление в Telegram')
        searching_parts()  # проверка на фрагменты перед загрузкой

        try:
            while True:
                subprocess_download(link)
                if searching_parts():  # проверка на фрагменты видео, если есть стереть и перекачать заново
                    continue
                else:
                    break
        except KeyboardInterrupt:
            try:
                telegram_send.send(
                    images=[image_read_from_db('interrupt')],
                    captions=[f'🔴Прерывание работы программы пользователем\n{time.strftime("%d.%m.%Yг., %H:%M:%S")}']
                )
            except:
                print('Не удалось отправить уведомление в Telegram')
            sys.exit('🔴 Прерывание работы программы пользователем')
        # Запись HTML файла с описанием
        write_html(path=path,
                   name=model,
                   link=link,
                   now_time=now_time,
                   attempt=attempt,
                   )
        # Сообщение об окончании загрузки
        message_finish_model_download = f"\n{SEPARATOR} Окончание загрузки модели {model.upper()} {SEPARATOR}" + '\n' * 10
        print(message_finish_model_download)


if __name__ == '__main__':
    print(prioritized_model_shuffle)
    print(dict_link)
    print(dict_path)
