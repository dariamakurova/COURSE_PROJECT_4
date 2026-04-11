from django.contrib import admin

from mailer.models import Client, Message


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "comment")
    list_filter = ("name",)
    search_fields = ("name", "email")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("title", "body")
    list_filter = ("title",)
    search_fields = ("title",)