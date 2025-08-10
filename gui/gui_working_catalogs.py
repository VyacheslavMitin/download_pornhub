import os


def open_catalog(dir_):
    """Функция открытия целевого каталога"""
    if os.name == 'posix':  # macos
        import subprocess
        subprocess.call(['open', dir_])
    elif os.name == 'nt':  # windows
        os.startfile(dir_)
    else:
        pass


def human_read_format(size):
    """Функция человеко-читаемого размера файлов"""
    sizes = [' Б', ' КБ', ' МБ', ' ГБ']
    index = 0
    for i in range(len(sizes)):
        if size / (1024 ** i) < 1:
            break
        index = i
    # return f'{round(size / (1024 ** index))}{sizes[index]}'
    return f'{(size / (1024 ** index)):.2f}{sizes[index]}'.replace(".", ",")


def get_directory_size(path='/Volumes/Seagate_2TB/backup/PornHub') -> int:
    """Функция расчета размера каталога"""
    import os

    total_size = 0
    try:
        for dir_path, dir_names, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dir_path, f)
                size = os.path.getsize(fp)
                total_size += size
    except PermissionError as e:
        print(f"Ошибка доступа к папке: {e}")
    except FileNotFoundError as f:
        print(f"Ошибка доступа к файлу: {f}")
    return total_size


def print_all_subdirectories(root_path='/Volumes/Seagate_2TB/backup/PornHub'):
    for root, dirs, files in os.walk(root_path):
        if len(files) > 0: # ищем только каталоги с файлами
            print(f"Каталог: {root}")
            print(f"Размер каталога: {human_read_format(get_directory_size(root))}")



def dict_for_buttons(root_path='/Volumes/Seagate_2TB/backup/PornHub') -> dict:
    dict_ = {}
    for root, dirs, files in os.walk(root_path):
        if len(files) > 0: # ищем только каталоги с файлами
            dict_[os.path.basename(root)] = [root,
                                             human_read_format(get_directory_size(root))
                                             ]
    return dict_

# DICT_ = dict_for_buttons()

if __name__ == '__main__':
    # Пример использования
    # print_all_subdirectories(root_path='/Volumes/Seagate_2TB/backup/PornHub')
    # print(DICT_)
    pass