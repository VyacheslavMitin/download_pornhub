# Функция проверки не полностью скаченных файлов, проверка наличия фрагментов от youtube-dl
import glob


def searching_parts():
    search_part = glob.glob("*.part")

    if search_part:
        print("\nНайдены незавершенные загрузки!\n".upper())

    return search_part
