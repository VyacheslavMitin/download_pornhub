# Модуль проверки дублирующих роликов по ID
import os
import random
import pprint

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
        list2 = []
        print(f"Обнаружены дубли файлов в количестве '{len(dict_doub)}' штук")
        pprint.pprint(dict_doub)
        for i in dict_doub.values():
            *garb, file_doub = i.split('/')
            list2.append(file_doub)
        tg_send_notifications_message(f"🟨 Обнаружены дубли файлов:\n"
                                      f"{list2}")


if __name__ == '__main__':
    model = 'blondessa'
    # dirs = os.path.join('Y:\\backup\\PornHub')
    # for item in os.listdir(dirs):
    #     if os.path.isdir(f'Y:\\backup\\PornHub\\{item}'):
    #         print(f'Y:\\backup\\PornHub\\{item}')
    #         check_doubles(path_to_model=f'Y:\\backup\\PornHub\\{item}')
    check_doubles(path_to_model=f'Y:\\backup\\PornHub\\{model}')
