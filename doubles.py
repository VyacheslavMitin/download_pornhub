# Модуль проверки дублирующих роликов по ID
# TODO сделать функцию и ей скармливать каталог в параметрах, проверять и индивидуально с уведомлениями по моделям и по всем сразу
import os
import random
import pprint

path_ = os.path.join('//KEENETIC_ULTRA/Seagate_2TB/backup/PornHub/')
list_ = []
dict_paths = {}

for item in os.listdir(path_):
    if os.path.isdir(os.path.join(path_, item)):
        list_.append(item)

pprint.pprint(list_)

for item in list_:
    dict_paths[item] = os.path.join(path_, item)

pprint.pprint(dict_paths)


dict_uniq = {}
dict_doub = {}

for path in dict_paths.values():
    for file in os.listdir(path):
        if file.endswith('.mp4'):
            file_ = file[-19:]
            file_ = file_[1:-5]
            if file_ not in dict_uniq.keys():
                dict_uniq[file_] = file
            else:
                dict_doub[f"{file_}-{random.randint(100,999)}"] = file

# print("Вывод словарей как есть")
# print("Уникальные")
# pprint.pprint(dict_uniq)
if dict_doub:
    print("Дубли")
    pprint.pprint(dict_doub)

# print("Вывод списка как есть")
# pprint.pprint(sorted(list_))

# with open('output.txt', 'w') as file:
#     for i in sorted(list_):
#         file.write(i + '\n')

# list_uniq = []
#
# for item in list_:
#     if item not in list_uniq:
#         list_uniq.append(item)
#     else:
#         print(f"Дублирующий элемент! {item}")
