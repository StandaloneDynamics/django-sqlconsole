from django import forms


class ConsoleForm(forms.Form):
    query = forms.CharField(widget=forms.Textarea(attrs={"cols": "160", "rows": "10"}))
