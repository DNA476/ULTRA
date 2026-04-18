from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email', 'city', 'created_at')
    list_filter = ('city', 'created_at')
    search_fields = ('name', 'contact_person', 'phone', 'email', 'city')
    readonly_fields = ('created_at', 'updated_at')
