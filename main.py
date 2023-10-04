# Модуль для скачки с pornhub, в зависимостях ytp-dl как отдельная программа в PATH
# Зависимости
# pip3 install telegram-send ; pip3 install --force-reinstall -v "python-telegram-bot==13.5" ; telegram-send --configure
import time
from links import RETURN_MODELS
from downloader import starting_download
import telegram_send

__version__ = '3.1.0'

now_time = time.strftime("%d.%m.%Yг., %H:%M:%S")


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
                     f"Количество моделей для загрузки: {len(RETURN_MODELS):}\n\n" +
                     "Список моделей для скачки:".upper() +
                     f'\n{models_list()}')

    print(message_start)
    telegram_send.send(messages=[message_start])
    starting_download()


if __name__ == '__main__':
    # print(models_list())
    main()
