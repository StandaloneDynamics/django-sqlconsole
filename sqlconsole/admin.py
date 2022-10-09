from django.contrib import admin
from django.urls import path

from .views import ConsoleView

from .models import QueryLog


@admin.register(QueryLog)
class QueryLogAdmin(admin.ModelAdmin):
    list_display = ('query', 'state', 'created', 'created_by')

    def get_urls(self):
        urls = super().get_urls()
        console_url = [
            path('query/', self.admin_site.admin_view(ConsoleView.as_view()), name='console')
        ]
        return console_url + urls

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False