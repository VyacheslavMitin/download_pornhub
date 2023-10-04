def read_files(filename) -> list:
    """Функция чтения файлов"""
    list_ = []
    try:
        with open(filename, 'r') as models_file:
            for item in models_file:
                slice_item = item[:-1]  # удаление переноса строк
                list_.append(slice_item)
    except FileNotFoundError as err_FileNotFoundError:
        import sys
        print(err_FileNotFoundError)
        sys.exit('Файл не найден, выход с ошибкой')

    return list_


PORNSTARS = read_files('+pornstars.txt')
MODELS = read_files('+models.txt')
PRIORITY = read_files('+priority.txt')


def union_models(mode) -> list:
    """Функция подготовки списка моделей.

    Режимы 'sorted' или 'mixed'"""

    sets_models = (*PORNSTARS, *MODELS, *PRIORITY)
    united_list = list(sets_models)
    united_list.sort()  # отсортированный список
    def priority_models(list_):
        """Функция для работы  приоритетными (новыми) моделями"""
        for model in PRIORITY:
            list_.remove(model)
            list_.insert(0, model)

    match mode:
        case 'sorted':
            priority_models(united_list)
            return united_list
        case 'mixed':
            import random
            united_list_shuffle = united_list.copy()
            random.shuffle(united_list_shuffle)
            priority_models(united_list_shuffle)
            return united_list_shuffle


if __name__ == '__main__':
    # print(read_files('+pornstars.txt'))
    print('СОРТИРОВАНО ->', union_models(mode='sorted'))
    print('ПЕРЕМЕШАНО ->', union_models(mode='mixed'))
