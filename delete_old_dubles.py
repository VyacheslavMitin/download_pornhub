# Модуль УДАЛЕНИЯ старых файлов с одинаковым ID

from configs import PATH

import os
import re


def find_files_to_delete(root_folder):
    # Регулярное выражение для поиска любого содержимого в квадратных скобках в конце имени файла (с расширением)
    id_pattern = re.compile(r"\[(.+?)\](?:\..+)?$")

    # Словарь для хранения самого нового файла по каждому ID
    # Ключ: ID, значение: кортеж (путь к файлу, время модификации)
    files_by_id = {}
    files_to_delete = []

    # Рекурсивно обходим каталог
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            match = id_pattern.search(filename)
            if match:
                file_id = match.group(1)
                full_path = os.path.join(dirpath, filename)
                try:
                    mtime = os.path.getmtime(full_path)
                except FileNotFoundError as e:
                    print(e)
                if file_id not in files_by_id:
                    files_by_id[file_id] = (full_path, mtime)
                else:
                    current_saved_path, current_saved_mtime = files_by_id[file_id]
                    if mtime > current_saved_mtime:
                        # Новый файл новее, старый отметим на удаление
                        files_to_delete.append(current_saved_path)
                        files_by_id[file_id] = (full_path, mtime)
                    else:
                        # Новый файл старее — отметим на удаление новый
                        files_to_delete.append(full_path)

    return files_to_delete


def main():
    folder = PATH
    files_to_delete = find_files_to_delete(folder)

    if not files_to_delete:
        print("Старых дублирующих файлов не найдено.")
        return

    print("Найдены следующие файлы для удаления:")
    for f in files_to_delete:
        print(f)

    answer = input("\nПодтвердите удаление всех перечисленных файлов? (да/нет): ").strip().lower()
    if answer == "да":
        for f in files_to_delete:
            try:
                os.remove(f)
                print(f"Удалён файл: {f}")
            except Exception as e:
                print(f"Ошибка при удалении файла {f}: {e}")
        print("Удаление завершено.")
    else:
        print("Удаление отменено.")


if __name__ == "__main__":
    print("Поиск дублей файлов для удаления...")
    main()
