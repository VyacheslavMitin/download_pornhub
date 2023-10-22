# Модуль для определения свободного и занятого дискового пространства
import shutil

from configs import PATH
from write_html import human_read_format


# result = shutil.disk_usage(PATH)

# print(result)
# print(f"Общая память {result[0]}")
# print(f"Общая память {human_read_format(result[0])}")
# print(f"Использованная память {result[1]}")
# print(f"Использованная память {human_read_format(result[1])}")
# print(f"Свободная память {result[2]}")
# print(f"Свободная память {human_read_format(result[2])}")
#
# print(f"Из общей памяти '{human_read_format(result[0])}' на хранилище в '{PATH}' свободно '{human_read_format(result[2])}'")

def disk_free_space() -> str:
    """Функция определения свободного места на хранилище"""
    result = shutil.disk_usage(PATH)
    free_space = human_read_format(result[2])
    # print(f"Свободно на хранилище: {free_space}")
    return free_space


def disk_usage_all_info() -> str:
    """Функция получения всей информации по использованию хранилища для файлов"""
    result = shutil.disk_usage(PATH)
    # string_ = (f"Из общей памяти '{human_read_format(result[0])}' "
    #            f"на хранилище в '{PATH}' свободно '{human_read_format(result[2])}'"
    #            f" (использовано '{human_read_format(result[1])}')")
    string_ = f"Свободно: {human_read_format(result[2])} из {human_read_format(result[0])}"
    return string_


if __name__ == '__main__':
    print(disk_free_space())
    print(disk_usage_all_info())
