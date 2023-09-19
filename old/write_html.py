# write-html.py
import datetime
import os

name_html = '+info.html'


def write_html(path, name, link):
    """Функция записи HTML файла с информацией о файлах и загрузках"""
    file = open(f'{path}{os.sep}{name_html}', 'w')

    message = f"""<html>
    <head>Загрузка {name.upper()}</head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
    <body>
    <p>Ссылка <a href={link}>{link}</a></p>
    <p>Время начала загрузки: {datetime.datetime.now().strftime("%H:%M, %d.%m.%Y г.")}</p>
    </body>
    </html>"""

    file.write(message)
    file.close()
