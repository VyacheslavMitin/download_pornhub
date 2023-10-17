# Модуль скачивания аватарок
import os.path
import requests
from bs4 import BeautifulSoup

from dictionary_processing import dict_link
from configs import temp_dir


def download_avatars(verbose: bool = True,
                     dictionary: dict = dict_link) -> None:
    """Функция загрузки аватарок всех моделей"""
    if verbose:
        print('Модуль загрузки аватарок моделей с PornHub\n\n'.upper())

    if verbose:
        print('Создаем каталог для хранения аватарок\n')
    os.makedirs(os.path.normpath(temp_dir), exist_ok=True)  # создание каталога с аватарками если не существует

    for model, link in dictionary.items():
        if verbose:
            print(f'Загружаем файл аватара модели {model.upper()}, по ссылке: {link}')
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")
        avatar_get = soup.find('img',
                               {'id': 'getAvatar'})
        # if verbose:  # печать тега с ссылкой в коде страницы
        #     print(avatar_get)
        try:
            src = avatar_get.get('src')
            if verbose:
                print(f'Ссылка на аватар на PornHub: {src}')
            url_avatar = requests.get(src).content

            with open(f'{temp_dir}{model}.jpg', 'wb') as file_avatar:
                file_avatar.write(url_avatar)

        except AttributeError:  # проверка на ошибку отсутствия доступа к аватарке (мертвая ссылка и тд)
            if verbose:
                print(f'Аватар модели {model.upper()} не доступен!')

        finally:
            if verbose:
                if os.path.isfile(f'{temp_dir}{model}.jpg'):
                    print(f"Аватар модели {model.upper()} сохранен в файл '{model}.jpg'\n")
                else:
                    print(f'Аватар модели {model.upper()} по не известной причине не сохранен!\n')
    if verbose:
        print('Все аватары моделей загружены\n\n')


if __name__ == '__main__':
    download_avatars(verbose=True,  # пример использования
                     dictionary={'booty_ass':
                                 'https://www.pornhub.com/model/booty_ass/'})
    download_avatars()  # все модели
