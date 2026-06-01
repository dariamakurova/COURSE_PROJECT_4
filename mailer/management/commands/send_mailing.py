from django.core.management.base import BaseCommand, CommandError
from mailer.models import Mailing
from mailer.services import check_and_send_mailing


class Command(BaseCommand):
    help = 'Запускает рассылку по ID'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки')
        parser.add_argument(
            '--force',
            action='store_true',
            help='Принудительная отправка без проверки времени',
        )

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']
        force = options['force']

        try:
            mailing = Mailing.objects.get(pk=mailing_id)
        except Mailing.DoesNotExist:
            raise CommandError(f'Рассылка с ID {mailing_id} не найдена')

        self.stdout.write(f'Запуск рассылки #{mailing_id}...')
        self.stdout.write(f'Тема: {mailing.message.title if mailing.message else "Без темы"}')
        self.stdout.write(f'Получателей: {mailing.recipients.count()}')

        if force:
            self.stdout.write(self.style.WARNING('Принудительная отправка (без проверки времени)'))
            from mailer.services import send_mailing
            success_count, failed_count = send_mailing(mailing_id)
            self.stdout.write(self.style.SUCCESS(f'Отправлено успешно: {success_count}'))
            self.stdout.write(self.style.ERROR(f'Ошибок: {failed_count}'))
        else:
            success, message, success_count, failed_count = check_and_send_mailing(mailing_id)

            if success:
                self.stdout.write(self.style.SUCCESS(f'✓ {message}'))
            else:
                self.stdout.write(self.style.ERROR(f'✗ {message}'))