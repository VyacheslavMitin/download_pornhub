# Модуль для загрузки роликов с pornhub, в зависимостях ytp-dl как отдельная программа в PATH
# Минимальная версия Python - 3.10 (из-за match-case)
# Зависимости
# pip3 install telegram-send ; pip3 install --force-reinstall -v "python-telegram-bot==13.5" ; telegram-send --configure
# Необходимо иметь python-telegram-bot==13.5", на более высоких не работает модуль telegram-send
# https://pythonhosted.org/telegram-send/
# https://pythonhosted.org/telegram-send/api/
import os
import subprocess
import sys
import time
import telegram_send

from links import RETURN_MODELS
from downloader import starting_download
from image_path import return_image_path


__version__ = '3.5.2'


def models_list() -> str:
    """Функция подготовки текстового массива с моделями"""
    count = 0  # вывод списка моделей построчно с указанием номера в списке очередности
    models_strings = ''

    for item in RETURN_MODELS:
        count += 1
        model_string = f'{count:2} ~ {item}'
        models_strings += model_string + '\n'

    return models_strings


def main():
    """Основная функция"""
    try:  # проверка параметров запуска
        if sys.argv[1] == '--edit-models':
            print('Модуль загрузки видео с PornHub, правка списков моделей')
            changes = input('Необходимы правки списков моделей? Y/Д или N/Н: ')
            match changes:
                case 'y' | 'Y' | 'Д' | 'д' | 'l' | 'L':
                    for item in ['!priority.txt',
                                 '!models.txt',
                                 '!pornstars.txt']:
                        subprocess.Popen(['nano', item]).wait()
                    time.sleep(1)
                    print('Правки выполнены\n\n')
                    os.system('clear')
                case '' | None | 'N' | 'n' | 'н' | 'Н':
                    print('Без правок\n\n')
                    os.system('clear')

        if sys.argv[1] == '--no-questions':
            print('Без параметров запуска\n\n')

    except IndexError:  # обработка отсутствия передаваемого параметра
        pass

    message_start_print = ('Загрузка роликов с PornHub'.upper() + '\n' +
                           f'{time.strftime("%d.%m.%Yг., %H:%M:%S")}\n' +  # текущее время
                           f'Версия Python: {sys.version[:-35]}\n' +  # [:-35]
                           f'Версия программы {__version__}\n' +
                           f'Количество моделей для загрузки: {len(RETURN_MODELS):}\n\n' +
                           'Список моделей для загрузки:'.upper() + '\n' +
                           f'{models_list()}'
                           )

    message_start_send = (f'💦Загрузка роликов с PH\n'
                          f'{time.strftime("%d.%m.%Yг., %H:%M:%S")}\n'  # текущее время
                          f'Версия Python: {sys.version[:-79]}\n' +  # [:-35]
                          f'Версия программы {__version__}\n'
                          f'Количество моделей для загрузки: {len(RETURN_MODELS):}\n\n'
                          f'Список моделей для загрузки:\n'
                          f'{models_list()}'
                          )

    time.sleep(1)

    print(message_start_print)
    with open(return_image_path('logo'), 'rb') as logo:
        telegram_send.send(
            # messages=[message_start_send],
            captions=[message_start_send],
            images=[logo]
        )

    starting_download()

    print('Все успешно загружено', '\n' * 5)
    with open(return_image_path('done'), 'rb') as done:
        telegram_send.send(
            # messages=[f'☑️Все успешно загружено\n{time.strftime("%d.%m.%Yг., %H:%M:%S")}'],
            captions=[f'☑️Все успешно загружено\n'
                      f'{time.strftime("%d.%m.%Yг., %H:%M:%S")}'],
            images=[done]
        )

    sys.exit(0)  # выход


if __name__ == '__main__':
    main()
