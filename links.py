from pprint import pprint

NAMES = (
    'adventurescouple',
    'amadani',
    'aprileighteen',
    'arrestme',
    'behindthemaskk',
    'booty_ass',
    'bouncingfucks',
    'broudal',
    'comerzz',
    'daisydabs',
    'danika_mori',
    'denata',
    'egg2025',
    'like2fingers',
    'lindseylove',
    'loadsonlucy',
    'madeincanarias',
    'marshmallowpussy',
    'miss-fantasy',
    'njfromrus',
    'no1syg',
    'nofacegirl',
    'officialbf',
    'pareja-hub',
    'sexyyennifer',
    'svetlanalicious',
    'that_txguy',
    'theperfectcpl',
    'vampirecollective',
    'leolulu',
    'mysweetapple',
)


def return_path(name):
    path = f"/Users/sonic/PycharmProjects/download_pornhub/test/{name}"
    return path


def return_link(name):
    link = f"https://www.pornhub.com/model/{name}/videos/upload"
    return link


# DICT_LINKS = {
#     # "denata": (
#     #     "/Users/sonic/PycharmProjects/download_pornhub/test/denata",
#     #     "https://www.pornhub.com/model/denata/videos/upload"
#     # ),
#     'meredithmilf': (
#         "/Users/sonic/PycharmProjects/download_pornhub/test/meredithmilf",
#         "https://rt.pornhub.com/model/meredithmilf/videos/upload"
#     ),
#     'sonya-blaze': (
#         "/Users/sonic/PycharmProjects/download_pornhub/test/sonya-blaze",
#         "https://rt.pornhub.com/model/sonya-blaze/videos/upload"
#     ),
# }

DICT_LINKS = {}

for item in NAMES:
    DICT_LINKS.update({item: (return_path(item), return_link(item))})

pprint(DICT_LINKS)
