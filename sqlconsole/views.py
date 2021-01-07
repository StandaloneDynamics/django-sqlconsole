from django.shortcuts import render
from .forms import ConsoleForm
from django.db import connection, utils
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction


@transaction.non_atomic_requests
@staff_member_required
def console(request):
    if request.method == "POST":
        form = ConsoleForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            columns = []
            results = []
            message = ""
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                        results = cursor.fetchall()
                    else:
                        message = "Success"
            except (
                utils.InternalError,
                utils.ProgrammingError,
                utils.OperationalError,
            ) as error:
                message = error
            finally:
                return render(
                    request,
                    "admin/sqlconsole.djhtml",
                    {
                        "form": form,
                        "results": results,
                        "columns": columns,
                        "message": message,
                    },
                )

    else:
        form = ConsoleForm()
    return render(request, "admin/sqlconsole.djhtml", {"form": form})
