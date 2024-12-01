from .models import History
from django import forms
from .models import UserInput
from django.forms.widgets import FileInput

class UserInputForm(forms.ModelForm):
    files = forms.FileField(
        widget=forms.FileInput(attrs={'multiple': True}),  # Use a standard FileInput with multiple attribute
        required=False,
    )

    class Meta:
        model = UserInput
        fields = ['title', 'text_content']

class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ["project", "subject", "content", "file1", "file2"]