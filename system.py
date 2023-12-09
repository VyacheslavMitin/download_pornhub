# Модуль для системных проверок и функций
# TODO сделать проверки системные
import sys
import os

# test = os.system('yt-dlp')
# print(type(test))
# print(test)
#
# if test:
#     print(1)


def update_system_title(text):
    """Функция замены заголовка в консоли"""
    for i in range(5):
        # подстановка заголовка в терминал
        sys.stdout.write(text)


if __name__ == '__main__':
    progress = 'fdfdfdf'
    model = 'ffdfdf'
    update_system_title(f"\x1b]2;{progress}, модель {model.upper()}\x07")
