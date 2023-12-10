# Модуль для системных проверок и функций
import sys
import os

from configs import PATH, DATABASE_MODELS

REQUIRED_APPS = ('yt-dlp', 'ffmpeg', 'python3.11')
REQUIRED_MODULES = ('telegram-send', 'python-telegram-bot', 'beautifulsoup4', 'requests')


def check_apps():
    """Функция проверки доступности рекомендуемых приложений"""
    print("Проверка на доступ к требуемым программам\n".upper())

    for app in REQUIRED_APPS:
        if os.system(f"which '{app}'") is True:
            print(f"Приложение '{app}' не установлено!")
            sys.exit(1)
        else:
            print(f"Приложение '{app}' установлено")

    print("Проверка на доступ к требуемым программам пройдена\n".upper())


def check_paths():
    """Функция проверки доступности путей"""
    print("Проверка на доступ к требуемым путям\n".upper())

    if os.path.isfile(DATABASE_MODELS) is not True:
        print(f"Путь к '{DATABASE_MODELS}', выход с ошибкой!")
        sys.exit(1)
    else:
        print(f"Путь к '{DATABASE_MODELS}' доступен")

    if os.path.isdir(PATH) is not True:
        print(f"Путь к '{PATH}' не доступен, выход с ошибкой!")
        sys.exit(1)
    else:
        print(f"Путь к '{PATH}' доступен")

    print("Проверка на доступ к требуемым путям пройдена\n".upper())


def check_modules():
    """Функция проверки модулей"""
    print("Проверка на доступ к требуемым модулям\n".upper())

    for module_ in REQUIRED_MODULES:
        if os.system(f"pip3 show {module_}") == 256:
            print(f"Модуль '{module_}' не установлен, выход с ошибкой!")
            sys.exit(1)
        print('')

    print("Проверка на доступ к требуемым модулям пройдена\n".upper())


def update_system_title(text):
    """Функция замены заголовка в консоли"""
    for i in range(5):  # для надежности 5 раз
        # подстановка заголовка в терминал
        sys.stdout.write(f"\x1b]2;{text}\x07")


def check_all():
    """Объединенная функция проверки всего"""
    print("Проверки выполнения зависимостей и доступности для запуска программы\n".upper())

    check_apps()
    check_paths()
    check_modules()

    print("Проверки выполнения зависимостей и доступности для запуска программы выполнены успешно\n".upper())

    os.system('clear')  # очистка консоли


if __name__ == '__main__':
    check_all()
    print("Тест замены заголовка в консоли")
    progress = 'test/test'
    model = 'test'
    update_system_title(f"\x1b]2;{progress}, модель {model.upper()}\x07")
