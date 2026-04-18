from django.urls import path
from django.views.generic import TemplateView

from mailer import views
from mailer.views import (
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    ClientListView,
    ClientDetailView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    MessageListView,
    MessageDetailView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    MailingListView,
    MailingDetailView,
)

app_name = 'mailer'

urlpatterns = [
    # Главная страница (можно сделать как список рассылок или клиентов)
    path('', ClientListView.as_view(), name='main'),

    # URL-ы для модели Client
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    # URL-ы для модели Message
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    # URL-ы для модели Mailing
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
]