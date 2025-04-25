# Модуль рассылки уведомлений
# Необходимо установить модули нужных версий, для рассылки уведомлений в Telegram
# https://pypi.org/project/telegram-send/
# ИСПОЛЬЗОВАТЬ ПИТОН 3.11
# ДЕЛАТЬ НУЖНО В VENV
# pip3 install -r requirements.txt
# ИЛИ
# pip3 install telegram-send
# pip3 install --force-reinstall -v "telegram-send==0.34"
# pip3 install --force-reinstall -v "python-telegram-bot==13.5"
# Настройка привязки бота к системе
# ЭТО ТОЖЕ ДЕЛАТЬ НУЖНО В VENV
# telegram-send --configure
# Необходимо иметь python-telegram-bot==13.5", на свежих не работает модуль telegram-send и python выше 3.11 тоже
# https://pythonhosted.org/telegram-send/
# https://pythonhosted.org/telegram-send/api/


import telegram_send
import telegram  # для обработки исключений


def tg_send_notifications_images(
        # message=None, # сообщение отдельно от картинки, не используется в данной программе
        captions: str = None,  # подпись к картинкам, используется
        images=None,
        parse_mode: str = 'html',
):
    """Функция для рассылки уведомлений в Telegram с картинкой и подписью к ней"""
    if captions and images:
        try:
            telegram_send.send(
                captions=[captions],
                images=[images],
                parse_mode=parse_mode,
            )
        except telegram.error.BadRequest:
            print("Не удалось отправить уведомление в Telegram - слишком длинное сообщение")
        except telegram.error.NetworkError:  # Перехват исключения если API не доступно по сети
            print('Не удалось отправить уведомление в Telegram - проблемы с сетью')
        except telegram_send.telegram_send.ConfigError:
            print('Не удалось отправить уведомление в Telegram - проблемы с настройками модуля')

    else:
        print("Не хватает параметров для отправки уведомления в Telegram!")


def tg_send_notifications_message(message: str = None,
                                  parse_mode: str = 'html'):
    """Функция для рассылки сообщений в Telegram"""
    if message:
        try:
            telegram_send.send(
                messages=[message],
                parse_mode=parse_mode,
            )
        except telegram.error.BadRequest:
            print("Не удалось отправить сообщение в Telegram - слишком длинное сообщение")
        except telegram.error.NetworkError:  # Перехват исключения если API не доступно по сети
            print('Не удалось отправить сообщение в Telegram - проблемы с сетью')
        except telegram_send.telegram_send.ConfigError:
            print('Не удалось отправить уведомление в Telegram - проблемы с настройками модуля')
    else:
        print("Не хватает параметров для отправки сообщения в Telegram!")


if __name__ == '__main__':
    # Тест отправки уведомлений
    from database_module import image_read_from_db

    model = 'test'
    print("Тест отправки уведомлений в Телеграмм")
    tg_send_notifications_images(captions=f"test\n<a href='http://ya.ru'>{model}</a>",
                                 images=image_read_from_db('logo'))

    from configs import WEB_SERVER
    tg_send_notifications_message(message=f"<a href='http://{WEB_SERVER}/juicy-xenia/+info.html'>JUICY-XENIA</a>\n"
                                  )
