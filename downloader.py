# Модуль для работы с backend для загрузки
# Из-за очередной блокировки PH пришлось перейти на TOR в proxy, мост, но лучше использовать VPN:
# obfs4 122.199.22.246:5342 B74D6031E64A7EF8E362395A7D85E3E02E8C2EF8 cert=uQLASVwr7ysdti/7oxYIy3ntn3U1Spx4Bk9Jesec7gYrAjmK4oP/GEz2s3zeVvy3NHf5bA iat-mode=0
import os
import subprocess
import time
import sys

from write_html import write_html_model, NAME_HTML_MODEL
from check_fragments import searching_unfinished_downloads
from dictionary_processing import dict_link, dict_path
from database_module import avatar_read_from_bd, image_read_from_db, update_attempts
from telegram_notifications import tg_send_notifications_images, tg_send_notifications_message
from cookies import COMMAND_OPTIONS_ADD
from disk_usage import difference_used_sizes, get_directory_size, human_read_format
from configs import WEB_SERVER, temp_dir
from system import update_system_title
from check_doubles import check_doubles
from info_after_download import info_after_download
from delete_files import deleting_files_for_list, deleting_files_for_mask


COMMAND = "yt-dlp"  # команда для вызова youtube-dl или аналогов, должна находится в PATH
COMMAND_OPTIONS = [  # параметры для yt-dlp
    '--abort-on-unavailable-fragment',  # отмена загрузки если фрагмент не доступен
    # yt-dlp --proxy socks5://proxy.example.com:1080
    '--proxy', "socks5://127.0.0.1:9150/",  # использование прокси от TOR
    '-P', f'temp:{temp_dir}',  # использование временной папки на локальной машине
    '--no-mtime',
    # '--quiet',
    # '--progress',
]
# if sys.argv[1] == '--tor':
#     COMMAND_OPTIONS.append('--proxy')
#     COMMAND_OPTIONS.append("socks5://127.0.0.1:9150/")

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

    if not os.path.isdir(os.path.normpath(temp_dir)):
        # print('Создаем временный каталог для файлов\n')
        os.makedirs(os.path.normpath(temp_dir), exist_ok=True)  # создание каталога с аватарками если не существует

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

        # Очистка каталога с временными файлами
        for tmp_files in os.listdir(os.path.abspath(temp_dir)):
            os.remove(os.path.abspath(temp_dir) + '/' + tmp_files)

        count += 1  # счетчик скачиваемой модели
        progress = f'{count}/{len(prioritized_model_shuffle)}'
        update_system_title(f"{progress}, модель {model.upper()}")

        attempt = update_attempts(model)
        now_time = time.strftime("%d.%m.%Yг., %H:%M:%S")

        message_start_model_download_print = (f"{SEPARATOR_START} Загрузка {progress},"
                                              f" модель {model.upper()},"
                                              f" попытка {attempt} {SEPARATOR_START}\n"
                                              )
        # Отправка уведомления в ТГ о начале загрузки модели
        message_start_model_download_send = (f"🟢 Началась загрузка {progress}\n"
                                             f"{now_time}\n"
                                             # f"{time.strftime("%d.%m.%Yг., %H:%M:%S")}\n"
                                             # f"Модель <a href='{WEB_SERVER}/{model}/{NAME_HTML_MODEL}'>{model.upper()}"
                                             f"Модель <a href='{link}videos'>{model.upper()}"
                                             f"</a>\n"
                                             # f"Модель {model.upper()}\n"
                                             f"Попытка {attempt}\n"
                                             )
        print(message_start_model_download_print)

        tg_send_notifications_images(captions=message_start_model_download_send,
                                     images=avatar)

        searching_unfinished_downloads(path)  # проверка на фрагменты перед загрузкой

        try:
            # before_size = shutil.disk_usage(path)[2]  # запомнить размер каталога модели до загрузки
            before_size = get_directory_size(path)
        except FileNotFoundError as err:
            print(err)
            before_size = None

        try:
            while True:
                subprocess_download(link)
                if searching_unfinished_downloads(temp_dir):  # проверка на фрагменты видео,
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

        # высчитывание разницы размеров до и после
        after_size = get_directory_size(path)
        difference_size = difference_used_sizes(after=after_size, before=before_size)
        if not difference_size <= 128:        # Сообщение об окончании загрузки
            print(f"\n🟩 Загружено {human_read_format(difference_size)}, модель {model.upper()} 🟩")
            tg_send_notifications_message(f"🟩 Загружено: {human_read_format(difference_size)}")

        # проверка на файлы которые нужно стереть и их удаление
        deleting_files_for_list()
        deleting_files_for_mask()

        # проверка дублей
        check_doubles(path)

        # инфо по модели
        info_after_download(path_to_model=path, link=link, model_=model)

        message_finish_model_download = (
                    f"\n{SEPARATOR_END} Окончание загрузки модели {model.upper()} {SEPARATOR_END}\n\n\n")
        print(message_finish_model_download)

        # Запись HTML файла с описанием
        # write_html_model(
        #     path=path,
        #     name=model,
        #     link=link,
        #     now_time=now_time,
        #     attempt=attempt,
        #                  )


if __name__ == '__main__':
    from pprint import pprint

    print(f"Опции для загрузчика {COMMAND_OPTIONS}")
    print()
    # print(prioritized_model_shuffle)
    print()
    pprint(dict_link)
    print()
    pprint(dict_path)
