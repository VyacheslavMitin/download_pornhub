# Модуль работы с куками для сайта PH, по сути тут только COMMAND_OPTIONS_ADD
# Часть контента заблокирована для не друзей моделей.
# Чтобы обойти это можно подружившись на сайте и предоставив данные для авторизации.
# Есть несколько вариантов, можно предоставить логин и пароль, а можно предоставить куки файлы или доступ к браузеру
# https://www.reddit.com/r/youtubedl/wiki/cookies/
# Можно передавать куки как yt-dlp --cookies cookies.txt в виде файла.
# Можно брать данные из браузеров как yt-dlp --cookies-from-browser firefox

COMMAND_OPTIONS = [  # параметры для yt-dlp
    '--abort-on-unavailable-fragment',  # отмена загрузки если фрагмент не доступен
    # '--quiet',
    # '--progress'
]


COMMAND_OPTIONS_ADD = [  # единственное, что есть в этом модуле
    '--cookies-from-browser', 'firefox'  # получение кук из браузера
    # '--cookies', 'cookies.txt' # чтение специально подготовленного файла с куками
]


if __name__ == '__main__':
    if COMMAND_OPTIONS_ADD:
        COMMAND_OPTIONS = COMMAND_OPTIONS + COMMAND_OPTIONS_ADD
    print(COMMAND_OPTIONS)
