# Модуль для скачки с pornhub, в зависимостях ytp-dl как отдельная программа в PATH
# Зависимости
# pip3 install telegram-send ; pip3 install --force-reinstall -v "python-telegram-bot==13.5" ; telegram-send --configure
import os
import subprocess
import sys
import time
from links import RETURN_MODELS
from downloader import starting_download
import telegram_send

__version__ = '3.3.1'

now_time = time.strftime("%d.%m.%Yг., %H:%M:%S")

try:  # проверка параметров запуска
    if sys.argv[1] == '--edit-models':
        print(sys.argv[1])
        changes = input('Необходимы правки списков моделей? Y/Д или N/Н: ')
        match changes:
            case 'y' | 'Y' | 'Д' | 'д' | 'l' | 'L':
                for item in ['!priority', '!models.txt', '!pornstars.txt']:
                    subprocess.Popen(['nano', item]).wait()
                time.sleep(1)
                print('Правки выполнены\n\n')
                os.system('clear')
            case '' | None | 'N' | 'n' | 'н' | 'Н':
                # time.sleep(1)
                print('Без правок\n\n')
                os.system('clear')

    if sys.argv[1] == '--no-questions':
        print('Без параметров запуска\n\n')

except IndexError:  # обработка отсутствия передаваемого параметра
    pass


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
    message_start = ("Загрузка роликов с PornHub".upper() + '\n' +
                     f'{now_time}\n' +
                     f'Версия Python: {sys.version[:-35]}\n' +
                     f'Версия программы {__version__}\n' +
                     f"Количество моделей для загрузки: {len(RETURN_MODELS):}\n\n" +
                     "Список моделей для скачки:".upper() +
                     f'\n{models_list()}')

    time.sleep(1)
    print(message_start)
    telegram_send.send(messages=[message_start])
    starting_download()
    telegram_send.send(messages={f'Все успешно загружено\n{now_time}'})
    sys.exit(0)


if __name__ == '__main__':
    main()
