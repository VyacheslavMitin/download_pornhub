# Функция проверки недокачанных файлов

import glob
# import os

# os.chdir(os.path.join("/Volumes/WD_4TB/Гнуха/PornHub/wetslavs"))
# print("Текущая директория ", os.path.abspath(os.path.curdir))


def searching_parts():
    search_part = glob.glob("*.part")

    if search_part:
        print("\nНайдены незавершенные загрузки!\n".upper())

    return search_part
