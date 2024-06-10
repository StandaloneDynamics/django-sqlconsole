import csv

from django.db import connection
from django.http import HttpResponse
from sqlconsole.models import QueryLog


def create_csv(query_id, response: HttpResponse) -> HttpResponse:
    sql = QueryLog.objects.get(id=query_id).query

    with connection.cursor() as cursor:
        cursor.execute(sql)
        if cursor.description:
            columns = [col[0] for col in cursor.description]
            results = cursor.fetchall()

            writer = csv.writer(response)
            writer.writerow(columns)
            for row in results:
                writer.writerow(row)

    return response
