from django.forms import ModelForm

from mailer.models import Client


class ClientForm(ModelForm):
    class Meta:
        model = Client


class MessageForm(ModelForm):
    class Meta:
        model = Message