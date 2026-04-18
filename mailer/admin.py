from django.contrib import admin
from .models import Client, Message, Mailing

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'comment']
    search_fields = ['name', 'email']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['title', 'body']
    search_fields = ['title']

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_date', 'end_date', 'status', 'message']
    filter_horizontal = ['recipients']
    list_filter = ['status']