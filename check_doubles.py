# Модуль проверки дублирующих роликов по ID
import os
import random

from configs import doubles_log_file, doubles_log_dir
from telegram_notifications import tg_send_notifications_message, tg_send_notifications_images
from database_module import avatar_read_from_bd, image_read_from_db, update_attempts


def check_doubles(path_to_model):
    """Модуль ддя поиска дублей роликов в каталогах по коду [ID]"""
    list1 = []

    if not os.path.isdir(os.path.normpath(doubles_log_dir)):
        # print('Создаем временный каталог для файлов\n')
        os.makedirs(os.path.normpath(doubles_log_dir), exist_ok=True)  # создание каталога для дублей

    for obj in os.listdir(path_to_model):
        # print(obj)
        list1.append(path_to_model + '/'+ obj)

    dict_uniq = {}
    dict_doub = {}
    dict_doubles_telegram_links = {}
    list_for_tg_links = []
    for file in list1:
        if '._' not in file:  # проверка на скрытый файл
        # if (file.endswith('.mp4') or file.endswith('.mkv')) and file.startswith('._'):
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
        for key, val in dict_doub.items():
            counter += 1
            *garb, doubles = val.split('/')
            list_for_doubles.append(f"   {counter}. {doubles}\n")
            list_for_doubles_for_telegram.append(f"{counter}) {doubles}")
            file_name_, *garb = key.split('-')
            # f"Модель <a href='{link}'>{model.upper()}"
            dict_doubles_telegram_links[doubles] = f"<a href='https://www.pornhub.org/view_video.php?viewkey={file_name_}'>{doubles}</a>"
            list_for_tg_links.append(file_name_)

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

        # print(dict_doub)
        # print(dict_doubles_telegram_links)
        # list_for_doubles_for_telegram_with_links = []
        # for double in list_for_doubles_for_telegram:
        #     list_for_doubles_for_telegram_with_links.append(f'https://www.pornhub.org/view_video.php?viewkey={double}')
        # print(list_for_doubles_for_telegram_with_links)
        str_list_for_doubles_for_telegram_with_links = '\n'
        y = 0
        for key1, val1 in dict_doubles_telegram_links.items():
            y = y+1
            str_list_for_doubles_for_telegram_with_links += f"{y}. {val1}\n"
        # print(str_list_for_doubles_for_telegram_with_links)
        str_list_for_doubles_for_telegram = '\n'.join(list_for_doubles_for_telegram)  # костыль для красивого вывода в телеграм
        tg_send_notifications_message(f"🟨 Обнаружены дубли файлов в количестве '{len(dict_doub)}' штук:\n"
                                      # f"{str_list_for_doubles_for_telegram}")
                                      f"{str_list_for_doubles_for_telegram_with_links}")

        # tg_send_notifications_message(f"🟨 Обнаружены дубли файлов в количестве '{len(dict_doub)}' штук:\n")
        # for items in list_for_tg_links:
        #     tg_send_notifications_images(captions=f"Модель <a href='тест'>тест",
        #                                  images=image_read_from_db('interrupt'),
        #                                  parse_mode='html')
        # tg_send_notifications_images(captions=f"{str_list_for_doubles_for_telegram_with_links}",
        #                              images=image_read_from_db('interrupt'),
        #                              parse_mode='html')
        # import time
        # tg_send_notifications_images(captions=f'🔴 Прерывание работы программы пользователем\n'
        #                                       f'{time.strftime("%d.%m.%Yг., %H:%M:%S")}',
        #                              images=image_read_from_db('interrupt'))
        #
        # message_start_model_download_send = (
        #                                      # f'🟢 Началась загрузка {time.strftime("%d.%m.%Yг., %H:%M:%S")}\n'
        #                                      # f'{time.strftime("%d.%m.%Yг., %H:%M:%S")}\n'
        #                                      # f"Модель <a href='{WEB_SERVER}/{model}/{NAME_HTML_MODEL}'>{model.upper()}"
        #                                      f"Модель <a href='https://wiki.portal2.sr/.cfg_Filesvideos'>test"
        #                                      f"</a>\n"
        #                                      # f"Модель {model.upper()}\n"
        #                                      f"Попытка 1\n"
        #                                      )
        #
        # tg_send_notifications_message(message=message_start_model_download_send,
        #                              )


if __name__ == '__main__':
    # model = 'adaline-star'
    # check_doubles(path_to_model=f'/Volumes/Seagate_2TB/backup/PornHub/{model}')
    print("Запущена проверка дублей...")
    from dictionary_processing import dict_path
    for obj in dict_path:
        check_doubles(path_to_model=f'/Volumes/Seagate_2TB/backup/PornHub/{obj}')
    # pass

