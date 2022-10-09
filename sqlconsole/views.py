from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from .forms import ConsoleForm
from django.db import connection, utils

from django.views import View
from .models import State


class ConsoleView(PermissionRequiredMixin, View):
    template_name = 'admin/sqlconsole.djhtml'
    form_class = ConsoleForm
    permission_required = 'sqlconsole.can_execute_query'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            console_query = form.cleaned_data.get('query')
            message = ''
            columns = []
            results = []
            try:
                with connection.cursor() as cursor:
                    cursor.execute(console_query)
                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                        results = cursor.fetchall()
                    else:
                        message = "Success"
                    query.state = State.SUCCESS
                    query.created_by = request.user
                    query.save()
            except (utils.InternalError,
                    utils.ProgrammingError,
                    utils.OperationalError) as error:
                message = error
                query.state = State.ERROR
                query.created_by = request.user
                query.save()
            finally:
                return render(
                    request,
                    self.template_name,
                    {
                        "form": form,
                        "results": results,
                        "columns": columns,
                        "message": message,
                    },
                )
        else:
            errors = form.errors['query']
            return render(request, self.template_name, {'form': form, "message": errors})