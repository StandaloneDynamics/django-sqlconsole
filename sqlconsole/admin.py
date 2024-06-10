from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

from sqlconsole.views import ConsoleView
from sqlconsole.models import QueryLog
from sqlconsole.download import create_csv


@admin.register(QueryLog)
class QueryLogAdmin(admin.ModelAdmin):
    list_display = ('query', 'state', 'created_at', 'created_by')

    def get_urls(self):
        urls = super().get_urls()
        console_url = [
            path('query/', self.admin_site.admin_view(ConsoleView.as_view()), name='console'),
            path('download/<int:query_id>', self.admin_site.admin_view(self.download_results),
                 name='download-console-csv')
        ]
        return console_url + urls

    def download_results(self, request, query_id):
        response = HttpResponse(content_type='text/csv', )
        response['Content-Disposition'] = 'attachment; filename="download.csv"'
        return create_csv(query_id, response)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
