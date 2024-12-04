# from .models import History
# from django import forms
# from .models import UserInput
# from django.forms.widgets import FileInput

# # Custom widget for multiple file uploads
# class CustomMultipleFileInput(FileInput):
#     def __init__(self, attrs=None):
#         super().__init__(attrs)
#         self.attrs.update({'multiple': True})

# class UserInputForm(forms.Form):
#     title = forms.CharField(max_length=255)
#     text_content = forms.CharField(widget=forms.Textarea, required=False)
#     files = forms.FileField(
#         widget=CustomMultipleFileInput,  # Use the custom widget
#         required=False,
#     )

#     def clean_files(self):
#         files = self.files.getlist('files')  # Get list of uploaded files
#         for file in files:
#             if file.size > 5 * 1024 * 1024:  # 5 MB limit
#                 raise forms.ValidationError("File size must be less than 5 MB.")
#             if not file.name.lower().endswith(('.jpg', '.png', '.txt', '.pdf', '.doc', '.docx')):
#                 raise forms.ValidationError("Invalid file type.")
#         return files

# class HistoryForm(forms.ModelForm):
#     class Meta:
#         model = History
#         fields = ["project", "subject", "content", "file1", "file2"]

from django import forms
from .models import History

class UserInputForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter title',
        })
    )
    text_content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Enter your content here',
            'style': 'resize: vertical;'
        })
    )
    files = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'multiple': True,
            'style': '''
                border: 2px dashed #dee2e6;
                padding: 2rem;
                background-color: #f8f9fa;
                cursor: pointer;
            ''',
        }),
        help_text='Supported: JPG, PNG, TXT, PDF, DOC, DOCX (Max 5MB)'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Title'
        self.fields['text_content'].label = 'Content'
        self.fields['files'].label = 'Upload Files'

    def clean_files(self):
        files = self.files.getlist('files')
        for file in files:
            if file.size > 5 * 1024 * 1024:  # 5 MB limit
                raise forms.ValidationError("File size must be less than 5 MB.")
            if not file.name.lower().endswith(('.jpg', '.png', '.txt', '.pdf', '.doc', '.docx')):
                raise forms.ValidationError("Invalid file type.")
        return files

class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ["project", "subject", "content", "file1", "file2"]
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'file1': forms.FileInput(attrs={'class': 'form-control'}),
            'file2': forms.FileInput(attrs={'class': 'form-control'}),
        }