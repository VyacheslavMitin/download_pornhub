# Модуль для записи HTML файла с информацией по каталогу
import os
import time

from configs import PATH, WEB_SERVER, SYS_DIR
from dictionary_processing import prioritized_model_shuffle, dict_link
# from disk_usage import get_directory_size

NAME_HTML_MODEL = '+info.html'
end_line = '\n'


def models_list_html() -> str:
    """Функция подготовки текстового массива с моделями и их нумерацией"""
    count = 0  # вывод списка моделей построчно с указанием номера в списке очередности
    models_strings = ''
    for item in prioritized_model_shuffle:
        count += 1
        model_string = f'{count:2} ~ <a href="{WEB_SERVER}/{item}/{NAME_HTML_MODEL}">{item}</a>'
        models_strings += model_string + '\n'
    return models_strings


def models_list_html2() -> str:
    """Функция подготовки текстового массива с моделями и их нумерацией"""
    count = 0  # вывод списка моделей построчно с указанием номера в списке очередности
    models_strings = ''
    for item in prioritized_model_shuffle:
        link = dict_link.get(item)
        count += 1
        # model_string = f'{count:2} ~ <a href="{WEB_SERVER}/{item}/{NAME_HTML_MODEL}">{item}</a>'
        model_string = f'{count:2} ~ <a href="{link}">{item}</a>'
        models_strings += model_string + '\n'
    return models_strings


def write_html_index(root=PATH):
    """Функция создания HTML index.html"""
    path_to_index_html = f'{root}{os.sep}{SYS_DIR}{os.sep}index.html'
    file = open(path_to_index_html, 'w')

    html = f"""<html>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
    <title>Программа загрузки с PornHub</title>
    <head><h1>Программа загрузки с PornHub</h1></head>
    <body>
    <p>Время начала загрузки: {time.strftime("%d.%m.%Yг., %H:%M:%S")}</p>
    <p>Список моделей: <br>
    {models_list_html().replace(end_line, '<br>')}</p>
    </body>
    </html>"""

    file.write(html)
    file.close()


def write_html_model(path, name, link, now_time, attempt):
    """Функция записи HTML файла с информацией о файлах и загрузках"""

    file = open(f'{path}{os.sep}{NAME_HTML_MODEL}', 'w', encoding="utf-8")

    def human_read_format(size):
        """Функция человеко-читаемого размера файлов"""
        sizes = [' Б', ' КБ', ' МБ', ' ГБ']
        index = 0
        for i in range(len(sizes)):
            if size / (1024 ** i) < 1:
                break
            index = i
        return f'{round(size / (1024 ** index))}{sizes[index]}'
        # return f'{(size / (1024 ** index)):.2f}{sizes[index]}'

    def get_size_file_in_directory():
        """Функция получения размера файлов в каталоге"""
        size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    size += os.path.getsize(fp)
        except PermissionError as e:
            print(f"Ошибка доступа к папке: {e}")
        except FileNotFoundError as f:
            print(f"Ошибка доступа к файлу: {f}")
        return human_read_format(size)

    def amount_files_in_directory():
        """Функция получения размера файлов в каталоге"""
        amount_files = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                if f != NAME_HTML_MODEL:  # проверка на html файл и вычитание его из счетчика
                    amount_files += 1
        return amount_files

    def get_files_sizes_dates() -> str:
        """Функция вывода имен и размеров файлов в строках"""
        from os.path import getctime
        from datetime import datetime

        os.chdir(path)
        a = ''
        count = 1  # начинаем счетчик с 1
        for f in os.listdir():
            if os.path.isfile(f):
                if f != NAME_HTML_MODEL:  # проверка на существование html файл и удаление его из списка
                    file_date = datetime.fromtimestamp(getctime(f)).strftime("%d.%m.%Y, %H:%M")
                    file_size = human_read_format(os.path.getsize(f))
                    a += (f'{count}. {f} - {file_size} - '
                          f'{file_date}\n')  # Решетки ##### для будущей замены в HTML на br
                    count += 1
        return a

    message = f"""<html>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
    <title>Модель {name.upper()}</title>
    <head><h1>Модель {name.upper()}</h1></head>
    <body>
    <p><a href="..{os.sep}index.html">Возврат в index.html</a></p>
    <p><a href={link}>{link}</a></p>
    <p>Количество попыток загрузки - {attempt}</p>
    <p>Время начала загрузки: {now_time}<br>
    Время окончания загрузки: {time.strftime("%d.%m.%Yг., %H:%M:%S")}</p>
    <p>Количество файлов - {amount_files_in_directory()} шт.<br>
    Общий размер файлов - {get_size_file_in_directory()}</p>
    <p>Список файлов: <br>
    {get_files_sizes_dates().replace(end_line, '<br>')}</p>
    </body>
    </html>"""

    file.write(message)
    file.close()


if __name__ == '__main__':
    # write_html_index()
    print(models_list_html())
