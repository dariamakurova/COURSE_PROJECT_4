from django.utils import timezone

from mailer.models import Mailing


def update_mailing_status(mailing):
    """Обновляет статус рассылки на основе текущего времени"""
    now = timezone.now()

    if mailing.end_date < now:
        mailing.status = Mailing.Status.FINISHED
    elif mailing.start_date <= now <= mailing.end_date:
        if mailing.status != Mailing.Status.ACTIVE:
            mailing.status = Mailing.Status.ACTIVE
    elif mailing.start_date > now:
        if mailing.status != Mailing.Status.CREATED:
            mailing.status = Mailing.Status.CREATED

    mailing.save(update_fields=['status'])