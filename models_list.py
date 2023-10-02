PRIORITY = {
    'playboyandnympho',
    'casaltafoda',
    'juicy-xenia',
    'sofia-luvin',
}

MODELS = {
    # 'no1sygirl',
    'amyhide',
    'anja-amelia',
    'arrestme',
    'aryaholes',
    'behindthemaskk',
    'bellamurr',
    'booty_ass',
    'bootyass-girl',
    'candy-love',
    'casaltafoda',
    'cattly-angel',
    'dickforlily',
    'divine_tits',
    'egg2025',
    'emma-modric',
    'hansel-grettel',
    'hidden-kitten',
    'honey-sasha',
    'juicy-xenia',
    'kisankanna',
    'like2fingers',
    'littleprincess199',
    'loadsonlucy',
    'luxurymur',
    'mastophiliac',
    'mia-queen',
    'misslexa',
    'mynewprofession',
    'mysexymodel',
    'nini_divine',
    'papaxmama',
    'playboyandnympho',
    'satanikweed',
    'sexyyennifer',
    'sofia-luvin',
    'sonya-kalfa',
    'sweetie-fox',
    'that-tx-couple',
    'theperfectcpl',
    'thiccivelvet',
    'vampirecollective',
    'wetslavs',
    'wettmelons',
    'winterlotus',
}

PORNSTARS = {
    'ashley-rosi',
    'lindsey-love',
}


def union_models(mode) -> list:
    """Функция подготовки списка моделей.

    Режимы 'sorted' или 'mixed'"""

    sets_models = (*PORNSTARS, *MODELS, *PRIORITY)
    united_set = set()
    for item in sets_models:  # чтение распакованных множеств с добавлением объектов в новое множество
        united_set.add(item)
    united_list = list(united_set)
    united_list.sort()  # отсортированный список
    def priority_models(list_):
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
    print(union_models(mode='sorted'))
    print(union_models(mode='mixed'))
