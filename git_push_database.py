# Модуль для отправки в Гит (GitHub) базы данных, которая лежит не в проекте
# import os
import shutil

from configs import PLATFORM, DATABASE_MODELS, abs_path
# from telegram_notifications import tg_send_notifications


def git_push_db():
    """Функция для отправки базы данных в GIT"""
    print("Отправка базы данных с моделями в GIT")
    db = "models.db"

    match PLATFORM:
        case 'macbook':
            print("Копирование базы в каталог программы на Macbook")
            shutil.copy(DATABASE_MODELS, abs_path)
            # os.system(f"git add -u {db}")
            # os.system("git commit -m 'обновление БД в Git'")
            # os.system("git push")

        case 'wifi_router':
            import sys
            sys.exit("Запущено не на той платформе! Выход с ошибкой.")


if __name__ == '__main__':
    git_push_db()
