# Модуль возврата путей к изображению
import os.path

img_dir = os.path.join('/Users/sonic/PycharmProjects/download_pornhub/images/')


def return_image_path(model: str = 'dummy',
                      avatar: bool = False) -> str:
    """Функция передачи пути к изображению"""
    img = ''

    match avatar:
        case False:
            img = f'{img_dir}{model}.jpg'
        case True:
            img = f'{img_dir}avatars/{model}.jpg'

    if os.path.isfile(img):
        image_path = img
    else:
        from download_avatars import download_avatars
        from dictionary_processing import dict_link
        link = dict_link.get(model)
        download_avatars(verbose=False,
                         dictionary={model: link}
                         )
        if os.path.isfile(img):
            image_path = img
        else:
            print(f'Аватара модели {model.upper()} не существует, устанавливаю заглушку')
            image_path = f'{img_dir}dummy.jpg'

    return image_path


if __name__ == '__main__':
    print('Путь к пустышке')
    print(return_image_path(model='dummy'))
    print()
    print('Путь к аватарке')
    print(return_image_path(model='sweetie-fox',
                            avatar=True))
