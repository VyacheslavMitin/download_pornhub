# Программа для пакетной загрузки роликов с pornhub, в зависимостях yt-dlp как отдельная программа в PATH.
# Установка зависимостей pip install -r requirements.txt
# Используется база данных для хранения настроек, аватарок, приоритетов и прочего, а так же файл ini для хранения путей
# Включен модуль рассылки уведомлений через telegram (telegram _send)
# Минимальная версия Python - 3.10 (из-за match-case)
# Максимальная версия Python - 3.11 (из-за telegram-send)
# Включена рассылка через Telegram, подробнее о рассылке в соответствующем модуле
# Для моделей где требуется "дружба" необходимо подложить куки через команду 'yt-dlp --cookies cookies.txt'
# Подробное об аутентификации и авторизации в соответствующем модуле
# Из-за очередной блокировки PH пришлось перейти на TOR в proxy, мост, но лучше использовать VPN:
# obfs4 122.199.22.246:5342 B74D6031E64A7EF8E362395A7D85E3E02E8C2EF8 cert=uQLASVwr7ysdti/7oxYIy3ntn3U1Spx4Bk9Jesec7gYrAjmK4oP/GEz2s3zeVvy3NHf5bA iat-mode=0

import os
import sys
import time

# from timedinput import timedinput  # сторонний модуль для ввода с таймаутом

from downloader import starting_download
from telegram_notifications import tg_send_notifications_images, tg_send_notifications_message
from write_html import write_html_index, models_list_html
from disk_usage import difference_used_sizes, get_directory_size, human_read_format, disk_usage_all_info
from configs import PATH, WEB_SERVER, PLATFORM
from system import update_system_title, check_all

__version__ = '7.9'


def main():
    """Основная функция"""
    check_all()  # проверка перед запуском

    try:  # проверка параметров запуска
        if sys.argv[1] == '--edit-models':
            print('Модуль загрузки видео с PornHub, правка списков моделей')
            changes = input('Необходимы правки списков моделей? y/N: ').lower()
            # changes = timedinput('Необходимы правки списков моделей? y/N: ', timeout=3, default="N")
            match changes:
                case 'y' | 'д' | 'l':
                    from database_module import insert_new_model
                    insert_new_model()
                    time.sleep(1)
                    print('Правки выполнены\n\n')
                case '' | None | 'n' | 'н':
                    print('Без правок\n\n')

        elif sys.argv[1] == '--no-questions':
            print('Без параметров запуска\n\n')

        elif sys.argv[1] is None:
            pass

        for i in range(2):
            if PLATFORM == 'win-pc':
                os.system('cls')
            else:
                os.system('clear')

    except IndexError:  # обработка отсутствия передаваемого параметра
        pass

    from dictionary_processing import prioritized_model_shuffle

    def models_list() -> str:
        """Функция подготовки текстового массива с моделями и их нумерацией"""
        count = 0  # вывод списка моделей построчно с указанием номера в списке очередности
        models_strings = ''
        for item in prioritized_model_shuffle:
            count += 1
            model_string = f'{count:2} ~ {item}'
            models_strings += model_string + '\n'
        return models_strings

    from database_module import image_read_from_db
    message_start_print = ('💦 Загрузка роликов с PornHub'.upper() + '\n' +
                           f'{time.strftime("%d.%m.%Yг., %H:%M:%S")}\n' +  # текущее время
                           f'{disk_usage_all_info()}\n'  # определение свободного места
                           f'Платформа: {sys.platform}\n'
                           f'Версия Python: {sys.version[:7]}\n' +  # [:-35]
                           f'Версия программы: {__version__}\n' +
                           f'Количество моделей для загрузки: {len(prioritized_model_shuffle):}\n\n' +
                           'Список моделей для загрузки:'.upper() + '\n' +
                           f'{models_list()}'
                           )

    message_start_send = (f'💦 Загрузка роликов с PH\n'
                          f'{time.strftime("%d.%m.%Yг., %H:%M:%S")}\n'  # текущее время
                          f'{disk_usage_all_info()}\n'  # определение свободного места
                          f'Платформа: {sys.platform}\n'
                          f'Версия Python: {sys.version[:7]}\n' +  # [:-35]
                          f'Версия программы: {__version__}\n'
                          f'Количество моделей для загрузки: {len(prioritized_model_shuffle):}\n\n'
                          )

    message_models_send = (
        f'<a href="{WEB_SERVER}">Список моделей для загрузки:</a>\n\n'
        f'{models_list_html()}'
    )

    # Вывод в консоль и рассылка уведомлений в Телеграм о старте загрузки роликов
    print(message_start_print)
    tg_send_notifications_images(captions=message_start_send,
                                 images=image_read_from_db('logo'))
    tg_send_notifications_message(message=message_models_send)

    write_html_index()  # Записать Index.html

    # Начало загрузки
    before_size = get_directory_size(PATH)
    starting_download()  # ЗАГРУЗКА
    after_size = get_directory_size(PATH)
    difference_size = difference_used_sizes(after=after_size, before=before_size)

    all_done = (f'☑️ Все успешно загружено\n{time.strftime("%d.%m.%Yг., %H:%M:%S")}\n'
                f'{disk_usage_all_info()}\n'
                f'Было загружено: {human_read_format(difference_size)}'
                )
    print(all_done)
    update_system_title(f'☑️ Все успешно загружено')
    tg_send_notifications_images(captions=all_done,
                                 images=image_read_from_db('done'))

    sys.exit(0)  # выход


if __name__ == '__main__':
    main()
