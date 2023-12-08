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


def difference_used_sizes(before: int = 0, after: int = 0) -> str:
    """Функция определения разницы в занятом месте (объемы загруженного)"""
    difference = before - after
    # print(difference)
    result = human_read_format(difference)
    return result


if __name__ == '__main__':
    # print(difference_used_sizes(before=shutil.disk_usage(PATH)[2], after=(shutil.disk_usage(PATH)[2] - 5000000000)))
    print("Свободное место:")
    print(disk_free_space())
    print("Использование диска")
    print(disk_usage_all_info())
