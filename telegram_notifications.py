# Модуль рассылки уведомлений
# Необходимо установить модули нужных версий, для рассылки уведомлений в Telegram
# https://pypi.org/project/telegram-send/
# pip install -r requirements.txt
# ИЛИ
# pip3 install telegram-send
# pip3 install --force-reinstall -v "telegram-send==0.34"
# pip3 install --force-reinstall -v "python-telegram-bot==13.5"
# Настройка привязки бота к системе
# telegram-send --configure
# Необходимо иметь python-telegram-bot==13.5", на свежих не работает модуль telegram-send и python выше 3.11 тоже
# https://pythonhosted.org/telegram-send/
# https://pythonhosted.org/telegram-send/api/


import telegram_send
import telegram  # для обработки исключений

from configs import WEB_SERVER


def tg_send_notifications_images(
        # message=None, # сообщение от дельно от картинки, не используется в данной программе
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
    else:
        print("Не хватает параметров для отправки уведомления в Telegram!")


def tg_send_notifications_message(message: str = None, parse_mode: str = 'html'):
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
    else:
        print("Не хватает параметров для отправки сообщения в Telegram!")


if __name__ == '__main__':
    from database_module import image_read_from_db

    model = 'test'
    models = "<a href='ya.ru'>test<a/>"

    tg_send_notifications_images(captions=f"test\n<a href='http://ya.ru'>{model}</a>",
                                 images=image_read_from_db('logo'))

    tg_send_notifications_message(message=
                                  f"<a href='http://{WEB_SERVER}/juicy-xenia/+info.html'>JUICY-XENIA</a>\n"
                                  )
