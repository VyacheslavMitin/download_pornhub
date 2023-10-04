def read_files(filename) -> list:
    """Функция чтения файлов"""
    list_ = []  # создание пустого списка для дальнейшей работы

    try:
        with open(filename, 'r') as models_file:
            for item in models_file:
                if '\n' in item:  # проверка на перенос строк
                    item = item[:-1]  # удаление переноса строк
                list_.append(item)

    except FileNotFoundError as err_FileNotFoundError:
        import sys
        print(err_FileNotFoundError)
        sys.exit(f'Файл {filename} не найден, выход с ошибкой!')

    else:  # если не было исключения при работе с файлами моделей - почистить списки от пустых строк и прочего
        for item in list_:
            if item == '' or item == ' ':
                list_.remove(item)
            if '#' in item:
                list_.remove(item)

    return list_

# Чтение файлов в списки ля последующей обработки
PORNSTARS = read_files('+pornstars.txt')
MODELS = read_files('+models.txt')
PRIORITY = read_files('+priority.txt')


def union_models(mode='mixed') -> list:
    """Функция подготовки списка моделей.

    Режимы 'sorted' или 'mixed'"""

    tuple_models = *PORNSTARS, *MODELS, *PRIORITY  # создание кортежа из распакованных списков
    united_list = list(set(tuple_models))  # превращение в множество и потом в список
    united_list.sort()  # сортировка списка
    def priority_models(list_):
        """Функция для работы приоритетными (новыми) моделями"""
        for model in PRIORITY:
            list_.remove(model)  # удаление модели из общего списка
            list_.insert(0, model)  # добавление модели из приоритетного списка в начало общего списка

    match mode:
        case 'sorted':
            priority_models(united_list)  # работа по списку приоритетных моделей
            return united_list  # возвращение отсортированного в алфавитном порядке списка
        case 'mixed':
            import random
            united_list_shuffle = united_list.copy()  # копия списка для работы
            random.shuffle(united_list_shuffle)  # смешивание содержимого списка
            priority_models(united_list_shuffle)  # работа по списку приоритетных моделей
            return united_list_shuffle  # возвращение смешанного списка


if __name__ == '__main__':
    # print(read_files('+models.txt'))
    print('СОРТИРОВАНО ->', union_models(mode='sorted'))
    print('ПЕРЕМЕШАНО ->', union_models(mode='mixed'))
