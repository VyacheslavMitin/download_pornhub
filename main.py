# Модуль для скачки с pornhub, в зависимостях ytp-dl как отдельная программа в PATH
# "youtube-dl --external-downloader aria2c -i --console-title"

# Импорты
from links5 import return_models
from downloader2 import starting_download


def main():
    print("Загрузка роликов с PornHub".upper()),
    print(f"Количество моделей для загрузки: {len(return_models()):}\n")
    print("Список моделей для скачки:\n".upper(),
          *return_models(), sep='\n')
    starting_download()


if __name__ == '__main__':
    main()
