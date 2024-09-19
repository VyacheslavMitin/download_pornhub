# Модуль для определения свободного и занятого дискового пространства
import shutil

from configs import PATH


def human_read_format(size):
    """Функция человеко-читаемого размера файлов"""
    sizes = [' Б', ' КБ', ' МБ', ' ГБ']
    index = 0
    for i in range(len(sizes)):
        if size / (1024 ** i) < 1:
            break
        index = i
    # return f'{round(size / (1024 ** index))}{sizes[index]}'
    return f'{(size / (1024 ** index)):.2f}{sizes[index]}'


def disk_free_space() -> str:
    """Функция определения свободного места на хранилище"""
    result = shutil.disk_usage(PATH)
    free_space = human_read_format(result[2])
    # print(f"Свободно на хранилище: {free_space}")
    return free_space


def disk_usage_all_info() -> str:
    """Функция получения всей информации по использованию хранилища для файлов"""
    result = shutil.disk_usage(PATH)
    string_ = f"Свободно: {human_read_format(result[2])} из {human_read_format(result[0])}"
    return string_


def difference_used_sizes(before: float = 0, after: float = 0) -> float:
    """Функция определения разницы в занятом месте (объемы загруженного)"""
    difference = after - before
    return difference


def get_directory_size(path) -> int:
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
    return total_size


if __name__ == '__main__':
    # print(difference_used_sizes(before=shutil.disk_usage(PATH)[2], after=(shutil.disk_usage(PATH)[2] - 5000000000)))
    print("Размер каталога:")
    print(get_directory_size('Y:\\backup\\PornHub\\wetslavs'))
    print(f"Свободное место:")
    print(disk_free_space())
    print("Использование диска:")
    print(disk_usage_all_info())
    print(human_read_format(1330175074))
