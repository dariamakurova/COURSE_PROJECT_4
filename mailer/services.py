# mailer/services.py

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Mailing, MailingAttempt
import logging
import traceback

logger = logging.getLogger(__name__)


def send_mailing(mailing_id):
    """
    Функция для отправки рассылки
    Возвращает: (success_count, failed_count)
    """
    from .models import Mailing

    try:
        mailing = Mailing.objects.get(pk=mailing_id)
    except Mailing.DoesNotExist:
        logger.error(f'Рассылка #{mailing_id} не найдена')
        return 0, 0

    now = timezone.now()

    # Проверка: можно ли отправлять сейчас
    if not (mailing.start_date <= now <= mailing.end_date):
        error_msg = f'Отправка невозможна: текущее время {now.strftime("%d.%m.%Y %H:%M")} не входит в интервал рассылки'
        logger.error(f'Рассылка #{mailing_id}: {error_msg}')

        # Логируем попытку отправки с ошибкой (для всей рассылки)
        # Но по заданию лучше логировать для каждого клиента
        return 0, 0

    # Получаем всех получателей
    recipients = mailing.recipients.all()

    if not recipients.exists():
        logger.warning(f'Рассылка #{mailing_id}: нет получателей')
        return 0, 0

    success_count = 0
    failed_count = 0

    # Отправляем письма каждому получателю
    for client in recipients:
        try:
            # Формируем письмо
            subject = mailing.message.title if mailing.message else 'Без темы'
            message = mailing.message.body if mailing.message else 'Нет текста'

            # Отправляем письмо
            sent = send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False,
            )

            # Формируем ответ сервера (успех)
            server_response = f'Письмо успешно отправлено на {client.email} в {timezone.now().strftime("%d.%m.%Y %H:%M:%S")}'

            # Логируем успешную отправку
            MailingAttempt.objects.create(
                mailing=mailing,
                client=client,
                status='success',
                server_response=server_response
            )
            success_count += 1
            logger.info(f'Письмо отправлено: {client.email} (рассылка #{mailing_id})')

        except Exception as e:
            # Формируем подробный ответ об ошибке
            error_message = str(e)
            server_response = f'Ошибка при отправке на {client.email}: {error_message}'

            # Логируем ошибку
            MailingAttempt.objects.create(
                mailing=mailing,
                client=client,
                status='failed',
                server_response=server_response
            )
            failed_count += 1
            logger.error(f'Ошибка при отправке {client.email}: {error_message}')

    # Обновляем статус рассылки, если нужно
    if mailing.status == Mailing.Status.CREATED and success_count > 0:
        mailing.status = Mailing.Status.ACTIVE
        mailing.save(update_fields=['status'])

    return success_count, failed_count


def check_and_send_mailing(mailing_id):
    """
    Проверяет возможность отправки и отправляет рассылку
    Возвращает: (success, message, success_count, failed_count)
    """
    from .models import Mailing

    try:
        mailing = Mailing.objects.get(pk=mailing_id)
    except Mailing.DoesNotExist:
        return False, 'Рассылка не найдена', 0, 0

    now = timezone.now()

    # Проверяем время
    if now < mailing.start_date:
        return False, f'Рассылка ещё не началась. Начало: {mailing.start_date.strftime("%d.%m.%Y %H:%M")}', 0, 0

    if now > mailing.end_date:
        return False, f'Рассылка уже завершена. Окончание: {mailing.end_date.strftime("%d.%m.%Y %H:%M")}', 0, 0

    # Отправляем
    success_count, failed_count = send_mailing(mailing_id)

    if success_count > 0:
        return True, f'Отправлено успешно: {success_count}, ошибок: {failed_count}', success_count, failed_count
    else:
        return False, f'Не удалось отправить письма. Ошибок: {failed_count}', success_count, failed_count