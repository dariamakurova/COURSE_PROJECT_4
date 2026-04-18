from django.db import models

class Client(models.Model):
    """Модель получателя рассылки"""
    email = models.EmailField(verbose_name='e-mail', unique=True, help_text="Введите адрес электронной почты")
    name = models.CharField(max_length=150, verbose_name='Ф.И.О.', help_text="Введите Ф.И.О." )
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ['name']

class Message(models.Model):
    """Модель сообщения"""
    title = models.CharField(max_length=150, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма', null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['title']

from django.utils.translation import gettext_lazy as _


class Mailing(models.Model):
    """Модель рассылки"""
    start_date = models.DateTimeField(verbose_name='Время и дата начала рассылки')
    end_date = models.DateTimeField(verbose_name='Время и дата окончания рассылки')

    class Status(models.TextChoices):
        FINISHED = "FN", _("Завершена")
        CREATED = "CR", _("Создана")
        ACTIVE = "AC", _("Запущена")

    status = models.CharField(max_length=2, choices=Status.choices, default=Status.CREATED)
    message = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL,
        related_name="mailings",
        null=True,
        blank=True,
        verbose_name="Сообщение"
    )
    recipients = models.ManyToManyField(Client, verbose_name="Получатели", related_name="mailings")

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ['-start_date']