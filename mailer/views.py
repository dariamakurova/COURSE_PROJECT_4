from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from mailer.forms import ClientForm, MessageForm
from mailer.models import Client, Message


# Client Views

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailer/client_form.html'
    success_url = reverse_lazy('mailer:main')

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    raise_exception = True

    def get_success_url(self):
        return reverse('mailer:client_info', args=[self.kwargs.get('pk')])

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'catalog/client_confirm_delete.html'
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy('mailer:main')

class ClientListView(ListView):
    model = Client

# Message Views

class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailer/message_form.html'
    success_url = reverse_lazy('mailer:main')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    raise_exception = True

    def get_success_url(self):
        return reverse('mailer:message_info', args=[self.kwargs.get('pk')])


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'catalog/message_confirm_delete.html'
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy('mailer:main')


class MessageListView(ListView):
    model = Client