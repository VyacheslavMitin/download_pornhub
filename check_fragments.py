# Функция проверки не полностью скаченных файлов, проверка наличия фрагментов от youtube-dl и их удаление
import glob


def searching_parts() -> list:
    """Функция вставки данных в таблицу из специально подготовленного файла"""
    # Поиск фрагментов видео
    search_part = glob.glob("*.part")
    search_ytdl = glob.glob("*.ytdl")

    if search_part:
        print("\nНайдены незавершенные загрузки! Очистка от фрагментов и повторная загрузка файлов модели\n")
        import os  # удаление кусков видео, как правило, их нельзя загрузить из фрагментов
        for item in search_part:
            os.remove(item)
        for item in search_ytdl:
            os.remove(item)

    return search_part


if __name__ == '__main__':
    searching_parts()
