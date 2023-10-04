# Модуль для записи HTML файла с информацией по каталогу
import os
import time

NAME_HTML = '+info.html'


def write_html(path, name, link, now_time):
    """Функция записи HTML файла с информацией о файлах и загрузках"""

    file = open(f'{path}{os.sep}{NAME_HTML}', 'w')

    def human_read_format(size):
        """Функция человеко-читаемого размера файлов"""
        sizes = [' Б', ' КБ', ' МБ', ' ГБ']
        index = 0
        for i in range(len(sizes)):
            if size / (1024 ** i) < 1:
                break
            index = i
        return f'{round(size / (1024 ** index))}{sizes[index]}'

    def get_size_file_in_directory():
        """Функция получения размера файлов в каталоге"""
        size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                size += os.path.getsize(fp)
        return human_read_format(size)

    def amount_files_in_directory():
        """Функция получения размера файлов в каталоге"""
        amount_files = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                if f != NAME_HTML:  # проверка на html файл и вычитание его из счетчика
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
                if f != NAME_HTML:  # проверка на html файл и удаление его из списка
                    file_date = datetime.fromtimestamp(getctime(f)).strftime("%d.%m.%Y, %H:%M")
                    file_size = human_read_format(os.path.getsize(f))
                    a += f'{count}. {f} - {file_size} - {file_date}#####'  # Решетки ##### для будущей замены в HTML на br
                    count += 1
        return a

    message = f"""<html>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
    <title>Модель {name.upper()}</title>
    <head><h1>{name.upper()}</h1></head>
    <body>
    <p><a href={link}>{link}</a></p>
    <p>Время начала загрузки: {now_time}<br>
    Время окончания загрузки: {time.strftime("%d.%m.%Yг., %H:%M:%S")}</p>
    <p>Количество файлов {amount_files_in_directory()}<br>
    Общий размер файлов - {get_size_file_in_directory()}</p>
    <p>Список файлов: <br>
    {get_files_sizes_dates().replace('#####', '<br>')}</p>
    </body>
    </html>"""

    file.write(message)
    file.close()
