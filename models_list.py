MODELS = {
    'amyhide',
    'anja-amelia',
    'arrestme',
    'aryaholes',
    'behindthemaskk',
    'bellamurr',
    'booty_ass',
    'bootyass-girl',
    'cattly-angel',
    'dickforlily',
    'divine_tits',
    'egg2025',
    'emma-modric',
    'hansel-grettel',
    'hidden-kitten',
    'honey-sasha',
    'kisankanna',
    'like2fingers',
    'littleprincess199',
    'loadsonlucy',
    'mastophiliac',
    'mia-queen',
    'misslexa',
    'mynewprofession',
    'mysexymodel',
    'nini_divine',
    # 'no1sygirl',
    'satanikweed',
    'sexyyennifer',
    'sonya-kalfa',
    'sweetie-fox',
    'that-tx-couple',
    'theperfectcpl',
    'thiccivelvet',
    'vampirecollective',
    'wetslavs',
    'wettmelons',
    'winterlotus',
    'papaxmama',
    'luxurymur',
    'candy-love',
}

PORNSTARS = {
    'ashley-rosi',
    'lindsey-love',
}


UNION_SET_MODELS = MODELS.union(PORNSTARS)
UNION_LIST_MODELS = list(UNION_SET_MODELS)
UNION_LIST_MODELS.sort()
import random
UNION_LIST_MODELS_SHUFFLE = UNION_LIST_MODELS.copy()
random.shuffle(UNION_LIST_MODELS_SHUFFLE)


if __name__ == '__main__':
    import pprint
    pprint.pprint(UNION_LIST_MODELS)
    print('+'*50)
    pprint.pprint(UNION_LIST_MODELS_SHUFFLE)

