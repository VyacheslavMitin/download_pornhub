# Программа для пакетной загрузки роликов с pornhub, в зависимостях yt-dlp как отдельная программа в PATH
# Используется база данных для хранения настроек, аватарок, приоритетов и прочего, а так же файл ini для хранения путей
# Включен модуль рассылки уведомлений через telegram (telegram _send)
# Минимальная версия Python - 3.10 (из-за match-case)
# Зависимости
# pip3 install telegram-send ; pip3 install --force-reinstall -v "python-telegram-bot==13.5" ; telegram-send --configure
# Подробнее о рассылке в соответствующем модуле
# Для моделей где требуется "дружба" необходимо подложить куки через команду 'yt-dlp --cookies cookies.txt'
# Подробное о аутентификации и авторизации в соответствующем модуле

import os
import sys
import time

from telegram_notifications import tg_send_notifications

__version__ = '4.4'


def main():
    """Основная функция"""
    try:  # проверка параметров запуска
        if sys.argv[1] == '--edit-models':
            print('Модуль загрузки видео с PornHub, правка списков моделей')
            changes = input('Необходимы правки списков моделей? y/N: ').lower()
            match changes:
                case 'y' | 'д' | 'l':
                    from database_module import insert_new_model_in_db
                    insert_new_model_in_db()
                    time.sleep(1)
                    print('Правки выполнены\n\n')
                    os.system('clear')
                case '' | None | 'n' | 'н':
                    print('Без правок\n\n')
                    os.system('clear')

        elif sys.argv[1] == '--no-questions':
            print('Без параметров запуска\n\n')

        elif sys.argv[1] is None:
            pass

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
    message_start_print = ('Загрузка роликов с PornHub'.upper() + '\n' +
                           f'{time.strftime("%d.%m.%Yг., %H:%M:%S")}\n' +  # текущее время
                           f'Версия Python: {sys.version[:-35]}\n' +  # [:-35]
                           f'Версия программы {__version__}\n' +
                           f'Количество моделей для загрузки: {len(prioritized_model_shuffle):}\n\n' +
                           'Список моделей для загрузки:'.upper() + '\n' +
                           f'{models_list()}'
                           )

    message_start_send = (f'💦Загрузка роликов с PH\n'
                          f'{time.strftime("%d.%m.%Yг., %H:%M:%S")}\n'  # текущее время
                          f'Версия Python: {sys.version[:-79]}\n' +  # [:-35]
                          f'Версия программы {__version__}\n'
                          f'Количество моделей для загрузки: {len(prioritized_model_shuffle):}\n\n'
                          f'Список моделей для загрузки:\n'
                          f'{models_list()}'
                          )

    print(message_start_print)
    tg_send_notifications(captions=message_start_send, images=image_read_from_db('logo'))

    from downloader import starting_download
    starting_download()

    print('Все успешно загружено', '\n' * 5)
    tg_send_notifications(captions=f'☑️Все успешно загружено\n{time.strftime("%d.%m.%Yг., %H:%M:%S")}',
                          images=image_read_from_db('done'))

    sys.exit(0)  # выход


if __name__ == '__main__':
    main()
