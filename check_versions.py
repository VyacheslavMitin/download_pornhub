# Модуль определения версий ПО

import subprocess

def get_command_version(command):
    try:
        result = subprocess.run([command, '--version'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Ошибка при выполнении команды: {e}"


version_info_python = get_command_version('python')
version_info_yt_dlp = get_command_version('yt-dlp')


if __name__ == '__main__':
    # Пример вызова
    # version_info_yt_dlp = get_command_version('yt-dlp')
    print(f"Версия Python: {version_info_python}")
    print(f"Версия YT-DLP: {version_info_yt_dlp}")
