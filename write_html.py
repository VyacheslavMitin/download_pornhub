# write-html.py
import datetime

name_html = '+info.html'


def write_html(path, name, link):
    file = open(f'{path}/{name_html}', 'w', encoding='utf-8')

    message = f"""<html>
    <head>Загрузка {name.upper()}</head>
    <body>
    <p>Ссылка <a href={link}>{link}</a></p>
    <p>Время начала загрузки: {datetime.datetime.now().strftime("%H:%M, %d.%m.%Y г.")}</p>
    </body>
    </html>"""

    file.write(message)
    file.close()
