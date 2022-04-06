#!/opt/bin/python
# Модуль скачки с порнхаба, в зависимостях aria2c и youtube-dl как отдельная программа в PATH
# "youtube-dl --external-downloader aria2c -i --console-title"

# Импорты
import os
import subprocess

from links import DICT_LINKS

COMMAND = (
    "youtube-dl",
    "--ignore-errors",
    "--no-warnings",
    "--external-downloader", "aria2c",
    "--external-downloader-arg",
    "--max-concurrent-downloads=5",
    # "--max-connection-per-server=5",
    # "--split=5",
    # "--min-split-size=1M",
)


print("Начало загрузки роликов\n".upper())

for model in DICT_LINKS.keys():
    PATH = os.path.join(DICT_LINKS.get(model)[0])
    LINK = DICT_LINKS.get(model)[1]

    if not os.path.isdir(PATH):
        os.mkdir(PATH)
    os.chdir(PATH)

    start_download = subprocess.call([
        *COMMAND,  # распаковка списка с командой youtube-dl
        LINK,  # передаваемая ссылка
    ])
