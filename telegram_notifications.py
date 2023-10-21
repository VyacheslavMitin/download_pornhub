# Модуль рассылки уведомлений
# pip3 install telegram-send ; pip3 install --force-reinstall -v "python-telegram-bot==13.5" ; telegram-send --configure
# Необходимо иметь python-telegram-bot==13.5", на свежих не работает модуль telegram-send и python выше 3.11 тоже
# https://pythonhosted.org/telegram-send/
# https://pythonhosted.org/telegram-send/api/

import telegram_send
import telegram  # для обработки исключений


def tg_send_notifications(
        # message=None, # сообщение от дельно от картинки, не используется в данной программе
        captions=None,  # подпись к картинкам, используется
        images=None):
    """Функция для рассылки уведомлений в Telegram с картинкой и подписью к ней"""
    if captions and images:
        try:
            telegram_send.send(
                # messages=[message],
                captions=[captions],
                images=[images],
            )
        except telegram.error.NetworkError:  # Перехват исключения если API не доступно по сети
            print('Не удалось отправить уведомление в Telegram')
    else:
        print("Не хватает параметров для отправки уведомления в Telegram!")


if __name__ == '__main__':
    from database_module import image_read_from_db
    tg_send_notifications(captions='test', images=image_read_from_db('logo'))
