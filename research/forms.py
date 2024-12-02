from .models import History
from django import forms
from .models import UserInput
from django.forms.widgets import FileInput

class UserInputForm(forms.ModelForm):
    class Meta:
        model = UserInput
        fields = ['title', 'text_content']  # Only the main fields

class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ["project", "subject", "content", "file1", "file2"]