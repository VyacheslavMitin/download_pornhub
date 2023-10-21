# Функция проверки не полностью скаченных файлов, проверка наличия фрагментов от youtube-dl и их удаление
import glob


def searching_unfinished_downloads() -> list:
    """Функция поиска файлов от неудачных загрузок видео модели"""
    # Поиск фрагментов видео
    search_part = glob.glob("*.part")
    search_ytdl = glob.glob("*.ytdl")

    mask = '.temp.'
    search_temp = glob.glob(f"*{mask}*")

    if search_part:  # работа с фрагментами видео
        print("\nОбнаружены незавершенные загрузки! Очистка от фрагментов и повторная загрузка файлов модели\n")
        import os  # удаление кусков видео, как правило, их нельзя загрузить из фрагментов
        for item in search_part:
            os.remove(item)
        for item in search_ytdl:
            os.remove(item)

    if search_temp:  # работа с временными файлами
        print("\nОбнаружен временный файл! "
              "Очистка от временного и связанного файлов и повторная загрузка файлов модели\n")
        import os
        for item_temp in search_temp:
            split1, split2 = item_temp.split(mask)
            item = f'{split1}.{split2}'
            files_tuple = (item, item_temp)
            try:
                for element in files_tuple:
                    os.remove(element)
            except FileNotFoundError:  # перехват исключения если файл не обнаружен
                pass

    return search_part


if __name__ == '__main__':
    searching_unfinished_downloads()
