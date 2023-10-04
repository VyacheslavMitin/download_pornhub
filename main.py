# Модуль для скачки с pornhub, в зависимостях ytp-dl как отдельная программа в PATH

from links import return_models
from downloader import starting_download

__version__ = 3.00

def main():
    """Основная функция"""
    print("Загрузка роликов с PornHub".upper()),
    print(f"Количество моделей для загрузки: {len(return_models()):}\n")
    print("Список моделей для скачки:".upper())
    # вывод списка моделей построчно с указанием номера в списке очередности
    count = 0
    for item in return_models():
        count += 1
        print(f'{count:2} ~ {item}')

    starting_download()


if __name__ == '__main__':
    main()
