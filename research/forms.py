from .models import History
from django import forms


class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ["project", "subject", "content", "file1", "file2"]