# Модуль уведомления по файлах модели после окончания загрузки
import os
from pathlib import Path

from disk_usage import get_directory_size, human_read_format
from telegram_notifications import tg_send_notifications_message


def info_after_download(path_to_model,link, model_='milfetta'):
    """Функция получения и высылки информации по модели"""
    path = Path(path_to_model)
    size = human_read_format(get_directory_size(path))
    files = []
    for i in os.listdir(path):
        if i.endswith('.mp4') or i.endswith('.mkv'):
            files.append(i)
    len_files = len(files)

    message = (f"\n🟣 Информация о модели {model_.upper()}:\n"
               f"Размер каталога: {size}\n"
               f"Количество роликов: {len_files}\n"
               f"Ссылка: {link}")
    print(f"{message}")
    tg_send_notifications_message(message)


if __name__ == '__main__':
    model = 'milfetta'
    link_test = f"https://pornhub.com/model/{model}/"
    info_after_download(path_to_model=f'Y:\\backup\\PornHub\\{model}', link=link_test)
