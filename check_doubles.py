# Модуль проверки дублирующих роликов по ID
import os
import random
# from distutils.command.clean import clean
# import pprint

from configs import doubles_log_file
from telegram_notifications import tg_send_notifications_message


def check_doubles(path_to_model):
    """Модуль ддя поиска дублей роликов в каталогах по коду [ID]"""
    list1 = []

    for obj in os.listdir(path_to_model):
        list1.append(path_to_model + '/'+ obj)

    dict_uniq = {}
    dict_doub = {}

    for file in list1:
        if file.endswith('.mp4') or file.endswith('.mkv'):
            file_ = file[-19:]  # отсечения кода ID со скобками
            file_ = file_[1:-5]  # вычленение кода
            if file_ not in dict_uniq.keys():
                dict_uniq[file_] = file
            else:
                dict_doub[f"{file_}-{random.randint(100,999)}"] = file

    if dict_doub:
        list_for_doubles = []
        list_for_doubles_for_telegram = []
        print(f"\n\nОбнаружены дубли файлов в количестве '{len(dict_doub)}' шт.:")
        chetchic = 0
        for i in dict_doub.values():
            chetchic += 1
            *garb, file_doub = i.split('/')
            list_for_doubles.append(f"   {chetchic}. {file_doub}\n")
            list_for_doubles_for_telegram.append(f"{chetchic}. {file_doub}")
        # list_for_doubles[0] = ' ' + list_for_doubles[0]  # при выводе в терминал добавить пробел чтобы выравнять строки
        # Добавление пробела в начало для нормального вывода списка
        list_for_doubles_for_print = list_for_doubles
        list_for_doubles_for_print[0] = ' ' + list_for_doubles_for_print[0]
        # print(*list_for_doubles_for_print)

        list_for_doubles_for_write = list_for_doubles
        list_for_doubles_for_write[0] = list_for_doubles_for_write[0][1:]
        # print(list_for_doubles_for_write)

        with open(doubles_log_file, 'a') as file:
            # file.write(f"Файл с дублями за {datetime.datetime.now().strftime('%d.%m.%Y')}\n\n")
            file.write(f"Модель: {path_to_model}\n")
            for el in list_for_doubles_for_write:
                file.write(el)
            file.write("\n\n")

        # clean_list_for_doubles = list_for_doubles
        # clean_list_for_doubles = [item[:-5] for item in clean_list_for_doubles]
        # print(clean_list_for_doubles)
        # print(list_for_doubles_for_telegram)
        str_list_for_doubles_for_telegram = '\n'.join(list_for_doubles_for_telegram)
        tg_send_notifications_message(f"🟨 Обнаружены дубли файлов в количестве '{len(dict_doub)}' штук:\n"
                                      f"{str_list_for_doubles_for_telegram}")


if __name__ == '__main__':
    model = 'adaline-star'
    # dirs = os.path.join('Y:\\backup\\PornHub')
    # for item in os.listdir(dirs):
    #     if os.path.isdir(f'Y:\\backup\\PornHub\\{item}'):
    #         print(f'Y:\\backup\\PornHub\\{item}')
    #         check_doubles(path_to_model=f'Y:\\backup\\PornHub\\{item}')
    # check_doubles(path_to_model=f'Y:\\backup\\PornHub\\{model}')
    check_doubles(path_to_model=f'/Volumes/Seagate_2TB/backup/PornHub/{model}')
