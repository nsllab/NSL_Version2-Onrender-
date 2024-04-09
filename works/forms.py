from django import forms
from .models import WeeklyReport, PostDocReport, Seminar, Review

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


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['write_date', 'update_date', 'tcp_ip', 'writer']

    subject = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 40}))


    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)