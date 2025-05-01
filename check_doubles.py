# Модуль проверки дублирующих роликов по ID
import os
import random

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
            file_ = file_[1:-5]  # вычленение кода ID
            if file_ not in dict_uniq.keys():
                dict_uniq[file_] = file
            else:
                dict_doub[f"{file_}-{random.randint(100,999)}"] = file

    if dict_doub:
        list_for_doubles = []
        list_for_doubles_for_telegram = []
        print(f"\n\nОбнаружены дубли файлов в количестве '{len(dict_doub)}' шт.:")
        counter = 0
        for i in dict_doub.values():
            counter += 1
            *garb, doubles = i.split('/')
            list_for_doubles.append(f"   {counter}. {doubles}\n")
            list_for_doubles_for_telegram.append(f"{counter}) {doubles}")

        list_for_doubles_for_print = list_for_doubles  # тут костыль для красивого вывода при выводе в терминал
        list_for_doubles_for_print[0] = ' ' + list_for_doubles_for_print[0]
        print(*list_for_doubles_for_print)

        list_for_doubles_for_write = list_for_doubles  # тут костыль для красивой записи в файл
        list_for_doubles_for_write[0] = list_for_doubles_for_write[0][1:]

        with open(doubles_log_file, 'a') as file:
            # file.write(f"Файл с дублями за {datetime.datetime.now().strftime('%d.%m.%Y')}\n\n")
            file.write(f"Модель: {path_to_model}\n")
            for el in list_for_doubles_for_write:
                file.write(el)
            file.write("\n\n")

        str_list_for_doubles_for_telegram = '\n'.join(list_for_doubles_for_telegram)  # костыль для красивого вывода в телеграм
        tg_send_notifications_message(f"🟨 Обнаружены дубли файлов в количестве '{len(dict_doub)}' штук:\n"
                                      f"{str_list_for_doubles_for_telegram}")


if __name__ == '__main__':
    model = 'adaline-star'
    check_doubles(path_to_model=f'/Volumes/Seagate_2TB/backup/PornHub/{model}')
