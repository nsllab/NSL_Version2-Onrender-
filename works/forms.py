from django import forms
from .models import WeeklyReport, PostDocReport, Seminar

class WeeklyReportForm(forms.ModelForm):
    class Meta:
        model = WeeklyReport
        exclude = ['user', 'writer']

class PostDocReportForm(forms.ModelForm):
    class Meta:
        model = PostDocReport
        exclude = ['user', 'writer']

class SeminarForm(forms.ModelForm):
    class Meta:
        model = Seminar
        # exclude = ['users', 'writer']
        fields = ['write_date', 'update_date', 'title', 'file1', 'file2']