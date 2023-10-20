# Модуль для загрузки роликов с pornhub, в зависимостях yt-dlp как отдельная программа в PATH, youtube-dl устарел
# Минимальная версия Python - 3.10 (из-за match-case)
# Зависимости
# pip3 install telegram-send ; pip3 install --force-reinstall -v "python-telegram-bot==13.5" ; telegram-send --configure
# Необходимо иметь python-telegram-bot==13.5", на свежих не работает модуль telegram-send и python выше 3.11 тоже
# https://pythonhosted.org/telegram-send/
# https://pythonhosted.org/telegram-send/api/
import os
import sys
import time
import telegram_send

from downloader import starting_download
from database_module import image_read_from_db
from dictionary_processing import prioritized_model_shuffle

__version__ = '4.3'


def main():
    """Основная функция"""
    try:  # проверка параметров запуска
        if sys.argv[1] == '--edit-models':
            print('Модуль загрузки видео с PornHub, правка списков моделей')
            changes = input('Необходимы правки списков моделей? y/N: ').lower()
            # TODO сделать инструкции по работе с базой sqlite
            match changes:
                case 'y' | 'д' | 'l':
                    # from dictionary_processing import prioritized_model_shuffle
                    # from database_module import insert_new_model_in_db
                    # insert_new_model_in_db()
                    time.sleep(1)
                    print('Правки выполнены\n\n')
                    os.system('clear')
                case '' | None | 'n' | 'н':
                    print('Без правок\n\n')
                    os.system('clear')

        if sys.argv[1] == '--no-questions':
            print('Без параметров запуска\n\n')

    except IndexError:  # обработка отсутствия передаваемого параметра
        pass

    def models_list() -> str:
        """Функция подготовки текстового массива с моделями и их нумерацией"""
        count = 0  # вывод списка моделей построчно с указанием номера в списке очередности
        models_strings = ''

        for item in prioritized_model_shuffle:
            count += 1
            model_string = f'{count:2} ~ {item}'
            models_strings += model_string + '\n'

        return models_strings

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
    try:
        telegram_send.send(
            captions=[message_start_send],
            images=[image_read_from_db('logo')]
        )
    except:
        print('Не удалось отправить уведомление в Telegram')
    starting_download()

    print('Все успешно загружено', '\n' * 5)
    try:
        telegram_send.send(
            captions=[f'☑️Все успешно загружено\n'
                      f'{time.strftime("%d.%m.%Yг., %H:%M:%S")}'],
            images=[image_read_from_db('done')]
        )
    except:
        print('Не удалось отправить уведомление в Telegram')

    sys.exit(0)  # выход


if __name__ == '__main__':
    main()
