from django import forms
from .models import QueryLog


class ConsoleForm(forms.ModelForm):
    query = forms.CharField(widget=forms.Textarea(attrs={"cols": "150", "rows": "10"}))

    class Meta:
        model = QueryLog
        fields = ('query', )

