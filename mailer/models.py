from django.db import models

class Client(models.Model):
    """Модель получателя рассылки"""
    email = models.EmailField(max_length=150, verbose_name='e-mail', unique=True, help_text="Введите адрес электронной почты")
    name = models.CharField(max_length=150, verbose_name='Ф.И.О.', help_text="Введите Ф.И.О." )
    comment = models.TextField(max_length=500, verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ['name']

class Message(models.Model):
    """Модель сообщения"""
    title = models.CharField(max_length=150, verbose_name='Тема письма')
    body = models.TextField(max_length=500, verbose_name='Тело письма', null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['title']
