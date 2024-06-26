from django import forms
from django.core.exceptions import ValidationError

from .models import QueryLog


class ConsoleForm(forms.ModelForm):
    query = forms.CharField(widget=forms.Textarea(attrs={"cols": "150", "rows": "10"}))

    class Meta:
        model = QueryLog
        fields = ('query',)

    def clean_query(self):
        sql = self.cleaned_data.get('query')
        sql = sql.lower()
        if 'update' in sql or 'delete' in sql or 'insert' in sql:
            raise ValidationError('Write queries not allowed')
        if ';' in sql:
            raise ValidationError('Multiple sql queries not allowed.')
        return sql
