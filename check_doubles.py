# Модуль проверки дублирующих роликов по ID
import os
import random
import pprint
from configs import PATH
from telegram_notifications import tg_send_notifications_images, tg_send_notifications_message


def check_doubles(path_to_model):
    list_ = []

    for item in os.listdir(path_to_model):
        list_.append(path_to_model + '/'+ item)

    print(list_)

    # for item in list_:
    #     dict_paths[item] = os.path.join(path_, item)
    #
    # pprint.pprint(dict_paths)

    dict_uniq = {}
    dict_doub = {}

    for file in list_:
        if file.endswith('.mp4'):
            file_ = file[-19:]
            file_ = file_[1:-5]
            if file_ not in dict_uniq.keys():
                dict_uniq[file_] = file
            else:
                dict_doub[f"{file_}-{random.randint(100,999)}"] = file

    if dict_doub:
        print("Обнаружены дубли файлов")
        pprint.pprint(dict_doub)
        tg_send_notifications_message(f"🔷 Обнаружены дубли:\n"
                                      f"{dict_doub}")


if __name__ == '__main__':
    model = 'blondessa'
    check_doubles(path_to_model=f'{PATH}/{model}')
