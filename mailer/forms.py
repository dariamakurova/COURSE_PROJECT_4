from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Client, Message, Mailing


class ClientForm(forms.ModelForm):
    """Форма для создания и редактирования клиента"""
    class Meta:
        model = Client
        fields = ['email', 'name', 'comment']

class MessageForm(forms.ModelForm):
    """Форма для создания и редактирования сообщения"""
    class Meta:
        model = Message
        fields = ['title', 'body']


class MailingForm(forms.ModelForm):
    """Форма для создания и редактирования рассылки"""

    class Meta:
        model = Mailing
        fields = ['start_date', 'end_date', 'message', 'recipients']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'message': forms.Select(attrs={'class': 'form-control'}),
            'recipients': forms.SelectMultiple(attrs={'class': 'form-control', 'size': 10}),
        }

    def clean(self):
        """Валидация дат"""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date <= start_date:
                raise ValidationError(
                    'Дата окончания должна быть позже даты начала рассылки'
                )

            if end_date < timezone.now():
                raise ValidationError(
                    'Дата окончания не может быть в прошлом'
                )

        return cleaned_data