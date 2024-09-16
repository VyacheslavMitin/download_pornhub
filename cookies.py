# Модуль работы с куками для сайта PH, по сути тут только COMMAND_OPTIONS_ADD
# Часть контента заблокирована для не друзей моделей.
# Чтобы обойти это можно подружившись на сайте и предоставив данные для авторизации.
# Есть несколько вариантов, можно предоставить логин и пароль, а можно предоставить куки файлы или доступ к браузеру
# https://www.reddit.com/r/youtubedl/wiki/cookies/
# Можно передавать куки как yt-dlp --cookies cookies.txt в виде файла.
# Можно брать данные из браузеров как yt-dlp --cookies-from-browser firefox

import os
from configs import PLATFORM

COMMAND_OPTIONS = [  # параметры для yt-dlp, в данном модуле только для примера
    '--abort-on-unavailable-fragment',  # отмена загрузки если фрагмент не доступен
]


def cookies_options() -> list:
    """Функция для определения откуда брать куки в зависимости от платформы"""
    list_ = []
    if os.path.isfile('cookies.txt'):  # проверка на наличие текстового файла с куками
        list_.append('--cookies')  # чтение специально подготовленного файла с куками
        list_.append('cookies.txt')
    else:  # если его нет попытка зайти через браузерные куки, но под платформы не настроено
        match PLATFORM:
            case 'mac':  # чтение кук их браузера, в данном случае из Firefox
                list_.append('--cookies-from-browser')
                list_.append('firefox')
            case 'wifi_router':  # чтение специально подготовленного файла с куками
                list_.append('--cookies')
                list_.append('cookies.txt')
            case 'win-pc':  # чтение специально подготовленного файла с куками
                list_.append('--cookies')
                list_.append('cookies.txt')

    return list_


COMMAND_OPTIONS_ADD = cookies_options()


if __name__ == '__main__':
    if COMMAND_OPTIONS_ADD:
        COMMAND_OPTIONS = COMMAND_OPTIONS + COMMAND_OPTIONS_ADD
    print(COMMAND_OPTIONS)
