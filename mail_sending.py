#Модуль для формирования и отправки писем
import os
import configparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Получение абсолютного пути к модулю
abs_path = os.path.abspath(os.curdir)
# Чтение конфигурации из файла ini
config_server = configparser.ConfigParser()
config_server.read('mail_settings.ini')

SERVER = config_server.get('SERVER',
                        'smtp_server')
PORT = int(config_server.get('SERVER',
                        'smtp_server_port'))

config_server = configparser.ConfigParser()
config_server.read('mail_credentials.ini')
LOGIN = config_server.get('CREDENTIALS',
                        'smtp_login')
PASSWORD = config_server.get('CREDENTIALS',
                        'smtp_password')
RECEIVER_EMAIL = config_server.get('CREDENTIALS',
                        'receiver_email')


def send_email(receiver_email=RECEIVER_EMAIL,
               subject="Модуль загрузки видео с PH",
               body="dummy"):
    # Ваши данные
    sender_email = LOGIN
    password = PASSWORD

    # Создание объекта MIMEMultipart
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Добавление текста письма
    message.attach(MIMEText(body, "plain"))

    # Отправка письма
    with smtplib.SMTP_SSL(SERVER, PORT) as server:
        try:
            server.login(sender_email, password)
            try:
                server.sendmail(sender_email, receiver_email, message.as_string())
            except Exception:
                print("Не удалось доставить письмо!")
            else:
                print(f"Отправлено письмо с отчетом о работе на '{RECEIVER_EMAIL}'")
        except Exception:
            print("Не произошло логина на почтовый сервер!")


if __name__ == '__main__':
    send_email(RECEIVER_EMAIL, "Модуль загрузки видео с PH", "Test")
