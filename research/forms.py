from .models import History
from django import forms
from .models import UserInput

class UserInputForm(forms.Form):
    title = forms.CharField(max_length=255)
    text_content = forms.CharField(widget=forms.Textarea, required=False)
    files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False,
    )

    def clean_files(self):
        files = self.files.getlist('files')
        for file in files:
            if file.size > 5 * 1024 * 1024:  # 5 MB limit
                raise forms.ValidationError("File size must be less than 5 MB.")
            if not file.name.lower().endswith(('.jpg', '.png', '.txt', '.pdf')):
                raise forms.ValidationError("Invalid file type.")
        return files

class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ["project", "subject", "content", "file1", "file2"]