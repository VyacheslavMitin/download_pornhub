# write-html.py
import os
import time

name_html = '+info.html'


def write_html(path, name, link, now_time):
    """Функция записи HTML файла с информацией о файлах и загрузках"""

    file = open(f'{path}{os.sep}{name_html}', 'w')

    def human_read_format(size):
        """Функция человеко-читаемого размера файлов"""
        sizes = [' Б', ' КБ', ' МБ', ' ГБ']
        index = 0
        for i in range(len(sizes)):
            if size / (1024 ** i) < 1:
                break
            index = i
        return f'{round(size / (1024 ** index))}{sizes[index]}'

    def get_size_file_in_direct():
        """Функция получения размера каталога"""
        size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                size += os.path.getsize(fp)
        return human_read_format(size)

    def get_files_sizes_dates() -> str:
        """Функция вывода имен и размеров файлов в строках"""
        from os.path import getctime
        from datetime import datetime

        os.chdir(path)
        a = ''
        count = 0
        for f in os.listdir():
            if os.path.isfile(f):
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
    <p>Время начала загрузки: {now_time} г. <br>
    Время окончания загрузки: {time.strftime("%d.%m.%Y г. %H:%M:%S")}</p>
    <p>Общий размер файлов - {get_size_file_in_direct()}</p>
    <p>Список файлов: <br>
    {get_files_sizes_dates().replace('#####', '<br>')}</p>
    </body>
    </html>"""

    file.write(message)
    file.close()
