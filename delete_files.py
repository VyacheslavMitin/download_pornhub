# Модуль для удаления файлов по маске или имени
import os
import glob

dir_names = ('honey-sasha',)
file_names = (
    'JOI. Instructions For Jerking Off. Do What I Tell You And You Will Definitely Cum [66f7eee74759b].mp4',
    'Kisankanna [ph5f42be50225fe].mp4',
    'Belle-mére en bas résille suce et se fait baiser son énorme cul chez moi! [ph5f4a44d33ab18].mp4',
    'belle-mère Française laisse son fils puceaux lui baiser son gros cul. [ph5f54cbba250ed].mp4',
    'Une gameuse joue, suce une bite et se fait prendre par derriere ! [ph5e36fbbfd4402].mp4',
    'Je baise le gros cul de ma Belle Mere et film! [ph5e6e4d053669f].mp4',
)
file_masks = (
    '._*',
)


def deleting_files_for_list():
    """Функция удаления файлов по списку имен"""
    # current_directory = os.path.basename(os.getcwd())  # получение имени текущего каталога
    current_directory = ''
    try:
        current_directory = os.path.basename(os.getcwd())
    except FileNotFoundError as fe:  # Исключение при несуществующем файле
        print(f"Каталог не найден: {fe}")

    if current_directory in dir_names:
        for file in file_names:
            if os.path.isfile(file):
                try:
                    os.remove(file)
                    print(f"Попытка удалить дублирующий файл '{file}'")
                except Exception as e:  # Общее исключение для всех ошибок
                    print(f"Ошибка при удалении файла: {e}")
                except PermissionError as pe:  # Исключение при недостатке прав
                    print(f"Недостаточно прав для удаления файла: {pe}")
                except IsADirectoryError as ide:  # Исключение при попытке удалить директорию
                    print(f"Путь указывает на каталог: {ide}")
                except FileNotFoundError as fe:  # Исключение при несуществующем файле
                    print(f"Файл не найден: {fe}")
                except OSError as oe:  # Общее исключение для операционных систем
                    print(f"Ошибка операционной системы: {oe}")
    else:
        # print(f"Не в каталоге по списку")
        pass


def deleting_files_for_mask():
    """Функция удаления файлов по маске"""
    # current_directory = os.path.abspath(os.getcwd())
    current_directory = ''
    try:
        current_directory = os.path.basename(os.getcwd())
    except FileNotFoundError as fe:  # Исключение при несуществующем файле
        print(f"Каталог не найден: {fe}")

    glob_files = []
    for el in file_masks:
        glob_files += glob.glob(os.path.join(current_directory, el))

    for file in glob_files:
        if os.path.isfile(file):
            try:
                os.remove(file)
            except Exception as e:  # Общее исключение для всех ошибок
                print(f"Ошибка при удалении файла: {e}")
            except PermissionError as pe:  # Исключение при недостатке прав
                print(f"Недостаточно прав для удаления файла: {pe}")
            except IsADirectoryError as ide:  # Исключение при попытке удалить директорию
                print(f"Путь указывает на каталог: {ide}")
            except FileNotFoundError as fe:  # Исключение при несуществующем файле
                print(f"Файл не найден: {fe}")
            except OSError as oe:  # Общее исключение для операционных систем
                print(f"Ошибка операционной системы: {oe}")


if __name__ == '__main__':
    # deleting_files_for_list()
    deleting_files_for_mask()
