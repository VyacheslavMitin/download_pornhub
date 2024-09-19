# Модуль проверки дублирующих роликов по ID
import os
import random
import pprint
from configs import PATH
from telegram_notifications import tg_send_notifications_message


def check_doubles(path_to_model):
    list1 = []

    for item in os.listdir(path_to_model):
        list1.append(path_to_model + '/'+ item)

    dict_uniq = {}
    dict_doub = {}

    for file in list1:
        if file.endswith('.mp4'):
            file_ = file[-19:]  # отсечения кода ID со скобками
            file_ = file_[1:-5]  # вычленение кода
            if file_ not in dict_uniq.keys():
                dict_uniq[file_] = file
            else:
                dict_doub[f"{file_}-{random.randint(100,999)}"] = file

    if dict_doub:
        list2 = []
        print("Обнаружены дубли файлов")
        pprint.pprint(dict_doub)
        for i in dict_doub.values():
            *garb, file_doub = i.split('/')
            list2.append(file_doub)
        tg_send_notifications_message(f"🔷 Обнаружены дубли:\n"
                                      f"{list2}")


if __name__ == '__main__':
    model = 'blondessa'
    check_doubles(path_to_model=f'{PATH}/{model}')
