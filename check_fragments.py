# Функция проверки не полностью скаченных файлов, проверка наличия фрагментов от youtube-dl и их удаление
import glob
import os

def searching_unfinished_downloads(path) -> list:
    """Функция поиска файлов от неудачных загрузок видео модели"""
    # Поиск фрагментов видео, удаление кусков видео, как правило, их нельзя загрузить из фрагментов
    search_part = glob.glob(f"{os.path.join(path)}\*.part")
    # print(search_part)
    search_ytdl = glob.glob(f"{os.path.join(path)}\"*.ytdl")

    mask = '.temp.'
    search_temp = glob.glob(f"{os.path.join(path)}\"*{mask}*")

    if search_part or search_ytdl:  # работа с фрагментами видео
        print("\n💫 Обнаружены незавершенные загрузки! Очистка от фрагментов и повторная загрузка файлов модели\n")
        for item in search_part:
            os.remove(item)
        for item in search_ytdl:
            os.remove(item)

    if search_temp:  # работа с временными файлами
        print("\n💫 Обнаружен временный файл! "
              "Очистка от временного и связанного файлов и повторная загрузка файлов модели\n")
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
    print('Проверка фрагментов')
    if not searching_unfinished_downloads('C:\\Users\\sonic\\PycharmProjects\\download_pornhub\\tmp'):
        print('Фрагментов нет')
