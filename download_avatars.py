# Модуль скачивания аватарок
import os.path
import requests
from bs4 import BeautifulSoup

from links import RETURN_DICT_DOWNLOADS
DICT_MODELS_LINKS = {}
for model_, list_, in RETURN_DICT_DOWNLOADS.items():
    DICT_MODELS_LINKS.update({model_: list_[1]})
# print(DICT_MODELS_LINKS)

avatars_dir = os.path.join('/Users/sonic/PycharmProjects/download_pornhub/images/avatars/')


def download_avatars(verbose: bool = True,
                     dictionary: dict = DICT_MODELS_LINKS) -> None:
    """Функция загрузки аватарок всех моделей"""
    if verbose:
        print('Модуль загрузки аватарок моделей с PornHub\n\n'.upper())

    if verbose:
        print('Создаем каталог для хранения аватарок\n')
    os.makedirs(os.path.normpath(avatars_dir), exist_ok=True)  # создание каталога с аватарками если не существует

    for model, link in dictionary.items():
        if verbose:
            print(f'Загружаем файл аватара модели {model.upper()}, по ссылке: {link}')
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")
        avatar_get = soup.find('img',
                               {'id': 'getAvatar'})
        # if verbose:
        #     print(avatar_get)
        try:
            src = avatar_get.get('src')
            if verbose:
                print(f'Ссылка на аватар на PornHub: {src}')
            url_avatar = requests.get(src).content

            with open(f'{avatars_dir}{model}.jpg', 'wb') as file_avatar:
                file_avatar.write(url_avatar)

        except AttributeError:  # проверка на ошибку отсутствия доступа к аватарке (мертвая ссылка и тд)
            if verbose:
                print(f'Аватар модели {model.upper()} не доступен!')

        finally:
            if verbose:
                if os.path.isfile(f'{avatars_dir}{model}.jpg'):
                    print(f"Аватар модели {model.upper()} сохранен в файл '{model}.jpg'\n")
                else:
                    print(f'Аватар модели {model.upper()} по не известной причине не сохранен!\n')
    if verbose:
        print('Все аватары моделей загружены\n\n')


if __name__ == '__main__':
    download_avatars(verbose=True,
                     dictionary={'MISSLEXA': 'https://www.pornhub.com/model/misslexa/'}
                     )
    # download_avatars(verbose=True,
    #                  dictionary=DICT_MODELS_LINKS)
    download_avatars()  # все модели
