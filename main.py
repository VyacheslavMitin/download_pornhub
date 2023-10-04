# Модуль для скачки с pornhub, в зависимостях ytp-dl как отдельная программа в PATH

from links import return_models
from downloader import starting_download


def main():
    """Основная функция"""
    print("Загрузка роликов с PornHub".upper()),
    print(f"Количество моделей для загрузки: {len(return_models()):}\n")
    print("Список моделей для скачки:".upper())

    count = 0
    for item in return_models():
        count += 1
        print(f'{count:2} ~ {item}')

    starting_download()


if __name__ == '__main__':
    main()
