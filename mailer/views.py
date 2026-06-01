from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from mailer.forms import ClientForm, MessageForm, MailingForm
from mailer.models import Client, Message, Mailing

from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from .models import Mailing, Client


def dashboard(request):
    """Главная страница с аналитикой"""

    # Общее количество всех рассылок
    total_mailings = Mailing.objects.count()

    # Количество активных рассылок
    now = timezone.now()
    active_mailings = Mailing.objects.filter(
        start_date__lte=now,
        end_date__gte=now,
        status=Mailing.Status.ACTIVE
    ).count()

    # Общее количество уникальных получателей (клиентов)
    total_clients = Client.objects.count()

    # Дополнительная статистика для наглядности (опционально)
    completed_mailings = Mailing.objects.filter(
        end_date__lt=now
    ).count()

    planned_mailings = Mailing.objects.filter(
        start_date__gt=now
    ).count()

    # Последние 5 рассылок
    recent_mailings = Mailing.objects.all().order_by('-start_date')[:5]

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'total_clients': total_clients,
        'completed_mailings': completed_mailings,
        'planned_mailings': planned_mailings,
        'recent_mailings': recent_mailings,
        'now': now,
    }

    return render(request, 'mailer/dashboard.html', context)


# Client Views

class ClientCreateView(CreateView):
    """Создание нового клиента"""
    model = Client
    form_class = ClientForm
    template_name = 'mailer/client_form.html'
    success_url = reverse_lazy('mailer:client_list')

class ClientUpdateView(UpdateView):
    """Редактрирование клиента"""

    model = Client
    form_class = ClientForm
    template_name = 'mailer/client_form.html'
    raise_exception = True

    def get_success_url(self):
        return reverse('mailer:client_detail', args=[self.kwargs.get('pk')])

class ClientDeleteView(DeleteView):
    """Удаление клиента"""
    model = Client
    template_name = 'mailer/client_confirm_delete.html'
    raise_exception = True
    success_url = reverse_lazy('mailer:main')

    def get_success_url(self):
        return reverse_lazy('mailer:main')


# mailer/views.py

class ClientListView(ListView):
    """Список всех клиентов"""
    model = Client
    template_name = 'mailer/client_list.html'
    context_object_name = 'clients'
    ordering = ['name']


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
    success_url = reverse_lazy('mailer:message_list')



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
    context_object_name = 'messages'


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
        form.instance.status = Mailing.Status.CREATED
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_clients'] = Client.objects.all().order_by('name')
        return context


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

from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.urls import reverse

from .services import check_and_send_mailing


class MailingSendView(View):
    """Вьюха для ручного запуска рассылки"""

    def get(self, request, pk):
        mailing = Mailing.objects.get(pk=pk)

        # Проверяем и отправляем
        success, message, success_count, failed_count = check_and_send_mailing(pk)

        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

        # Добавляем информацию о количестве отправленных писем
        if success_count > 0 or failed_count > 0:
            messages.info(request, f'Отправлено успешно: {success_count}, ошибок: {failed_count}')

        return redirect('mailer:mailing_detail', pk=pk)