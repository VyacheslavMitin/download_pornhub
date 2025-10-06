import zipfile
import os
import shutil

from configs import PATH, SYS_DIR

# abs_path = os.path.abspath(os.curdir)

def zip_and_move(verbose=False):
    """Функция архивация и резервного копирования баз данных"""
    try:
        # Переход в каталог с файлами баз данных
        path_ = os.path.join(PATH, SYS_DIR)
        os.chdir(path_)

    except FileNotFoundError:
        print(f"Каталог '{path_}' не найден, выход с ошибкой")

    else:
        # Список файлов, которые нужно добавить в архив
        files_to_zip = ['models.db', 'models_test.db']

        # Имя создаваемого zip-архива
        zip_name = 'models_db.zip'

        # Создаем zip-архив в режиме записи ('w').
        # Режим 'w' автоматически перезаписывает файл, если он существует
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Добавляем каждый файл в архив
            for file in files_to_zip:
                zipf.write(file)

        # Получаем абсолютный путь к каталогу запуска скрипта
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Путь назначения архива - текущий каталог скрипта + имя архива
        destination_path = os.path.join(current_dir, zip_name)

        # Перемещаем архив в текущий каталог скрипта, перезаписывая при необходимости
        shutil.move(zip_name, destination_path)

        if verbose:
            print(f"Архив '{zip_name}' создан и перемещен")


if __name__ == '__main__':
    zip_and_move(verbose=True)
