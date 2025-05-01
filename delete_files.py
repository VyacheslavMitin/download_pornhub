# Модуль для удаления файлов по маске или имени
import os
import glob

dir_names = ('honey-sasha',)
file_names = ('JOI. Instructions For Jerking Off. Do What I Tell You And You Will Definitely Cum [66f7eee74759b].mp4',)
file_masks = ('._*', '.1_*')


def deleting_files_for_list():
    """Функция удаления файлов по списку имен"""
    current_directory = os.path.basename(os.getcwd())  # получение имени текущего каталога
    if current_directory in dir_names:
        for file in file_names:
            if os.path.isfile(file):
                try:
                    os.remove(file)
                    print(f"Попытка удалить дублирующий файл '{file}'")
                except FileNotFoundError as e:
                    print("Файл не найден.")
                except PermissionError as e:
                    print("Недостаточно прав для удаления файла.")
                except IsADirectoryError as e:
                    print("Путь указывает на каталог.")
                except OSError as e:
                    print(f"Ошибка операционной системы: {e}")
    else:
        # print(f"Не в каталоге по списку")
        pass


def deleting_files_for_mask():
    """Удаление файлов по маске"""
    current_directory = os.path.abspath(os.getcwd())
    # Получаем список всех файлов в указанной директории
    # file_list = [f for f in os.listdir(current_directory) if os.path.isfile(os.path.join(current_directory, f))]

    glob_files = []
    for el in file_masks:
        glob_files += glob.glob(os.path.join(current_directory, el))
    # print(glob_files)

    for file in glob_files:
        if os.path.isfile(file):
            try:
                os.remove(file)
            except FileNotFoundError:
                pass
            except PermissionError:
                pass
            except IsADirectoryError:
                pass
            except OSError:
                pass


if __name__ == '__main__':
    # deleting_files_for_list()
    deleting_files_for_mask()
