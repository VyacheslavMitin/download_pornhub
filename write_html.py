# write-html.py
import datetime


def write_html(path, name):
    file = open(f'{path}/info.html', 'w', encoding='utf-8')

    message = f"""<html>
    <head>Загрузка {name.upper()}</head>
    <body><p>Время начала загрузки: {datetime.datetime.now().strftime("%H:%M, %d.%m.%Y г.")}</p></body>
    </html>"""

    file.write(message)
    file.close()
