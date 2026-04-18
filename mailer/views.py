from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from mailer.forms import ClientForm, MessageForm, MailingForm
from mailer.models import Client, Message, Mailing


# Client Views

class ClientCreateView(CreateView):
    """Создание нового клиента"""
    model = Client
    form_class = ClientForm
    template_name = 'mailer/client_form.html'
    success_url = reverse_lazy('mailer:main')

class ClientUpdateView(UpdateView):
    """Редактрирование клиента"""

    model = Client
    form_class = ClientForm
    template_name = 'mailer/client_form.html'
    raise_exception = True

    def get_success_url(self):
        return reverse('mailer:client_info', args=[self.kwargs.get('pk')])

class ClientDeleteView(DeleteView):
    """Удаление клиента"""
    model = Client
    template_name = 'mailer/client_confirm_delete.html'
    raise_exception = True
    success_url = reverse_lazy('mailer:main')

    def get_success_url(self):
        return reverse_lazy('mailer:main')

class ClientListView(ListView):
    """Список всех клиентов"""
    model = Client
    template_name = 'mailer/client_list.html'


class ClientDetailView(DetailView):
    """Просмотр клиента"""
    model = Client
    template_name = 'mailer/client_detail.html'

# Message Views

class MessageCreateView(CreateView):
    """Создание сообщения"""
    model = Message
    form_class = MessageForm
    template_name = 'mailer/message_form.html'
    success_url = reverse_lazy('mailer:main')


class MessageUpdateView(UpdateView):
    """Редактирование сообщения"""
    model = Message
    form_class = MessageForm
    template_name = 'mailer/message_form.html'
    raise_exception = True

    def get_success_url(self):
        return reverse('mailer:message_info', args=[self.kwargs.get('pk')])


class MessageDeleteView(DeleteView):
    """Удаление сообщения"""
    model = Message
    template_name = 'mailer/message_confirm_delete.html'
    raise_exception = True
    success_url = reverse_lazy('mailer:main')

    def get_success_url(self):
        return reverse_lazy('mailer:main')


class MessageListView(ListView):
    """Список всех сообщений"""
    model = Message
    template_name = 'mailer/message_list.html'


class MessageDetailView(DetailView):
    """Просмотр сообщения"""
    model = Message
    template_name = 'mailer/message_detail.html'

# Mailing Views

class MailingCreateView(CreateView):
    """Создание новой рассылки"""
    model = Mailing
    form_class = MailingForm
    template_name = 'mailer/mailing_form.html'

    def get_success_url(self):
        return reverse('mailer:mailing_detail', args=[self.object.pk])

    def form_valid(self, form):
        """При создании статус всегда 'Создана'"""
        form.instance.status = Mailing.Status.CREATED
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    """Редактирование рассылки"""
    model = Mailing
    form_class = MailingForm
    template_name = 'mailer/mailing_form.html'

    def get_success_url(self):
        return reverse('mailer:mailing_detail', args=[self.object.pk])

    def form_valid(self, form):
        """При редактировании проверяем и обновляем статус"""
        mailing = form.save(commit=False)

        # Обновляем статус на основе дат
        now = timezone.now()
        if mailing.end_date < now:
            mailing.status = Mailing.Status.FINISHED
        elif mailing.start_date <= now <= mailing.end_date:
            mailing.status = Mailing.Status.ACTIVE
        elif mailing.start_date > now:
            mailing.status = Mailing.Status.CREATED

        return super().form_valid(form)


class MailingDeleteView(DeleteView):
    """Удаление рассылки"""
    model = Mailing
    template_name = 'mailer/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailer:mailing_list')


class MailingListView(ListView):
    """Список всех рассылок"""
    model = Mailing
    template_name = 'mailer/mailing_list.html'
    context_object_name = 'mailings'
    ordering = ['-start_date']  # сначала новые

    def get_queryset(self):
        """Обновляем статусы перед отображением списка"""
        queryset = super().get_queryset()
        for mailing in queryset:
            self._update_status(mailing)
        return queryset

    def _update_status(self, mailing):
        """Обновление статуса рассылки на основе текущего времени"""
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


class MailingDetailView(DetailView):
    """Просмотр рассылки"""
    model = Mailing
    template_name = 'mailer/mailing_detail.html'
    context_object_name = 'mailing'

    def get_object(self, queryset=None):
        """Обновляем статус при просмотре"""
        obj = super().get_object(queryset)
        self._update_status(obj)
        return obj

    def _update_status(self, mailing):
        """Обновление статуса рассылки"""
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
