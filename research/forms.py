from .models import History
from django import forms
from .models import UserInput

class UserInputForm(forms.ModelForm):
    class Meta:
        model = UserInput
        fields = ['title', 'text_content', 'file']

class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ["project", "subject", "content", "file1", "file2"]