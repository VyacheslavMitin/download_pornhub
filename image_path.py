# Модуль возврата путей к изображению
import os.path

img_dir = os.path.join('/Users/sonic/PycharmProjects/download_pornhub/images/')


def return_image_path(image: str = 'dummy', avatar: bool = False) -> str:
    """Функция передачи пути к изображению"""
    img = ''

    match avatar:
        case False:
            img = f'{img_dir}{image}.jpg'
        case True:
            img = f'{img_dir}avatars/{image}.jpg'

    if os.path.isfile(img):
        image_path = img
    else:
        image_path = f'{img_dir}dummy.jpg'

    return image_path


if __name__ == '__main__':
    print(return_image_path(image='dummy'))
    print(return_image_path(image='sweetie-fox',
                            avatar=True))
