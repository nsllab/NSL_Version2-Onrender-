from django.db import models
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import get_user_model

from members.models import Member

def get_default_user():
    return get_user_model().objects.get(username='admin').id

def default_from_date():
    return timezone.now() + timedelta(days=(0 - timezone.now().weekday()) % 7)

def next_friday():
    today = timezone.now()
    days_until_friday = (4 - today.weekday()) % 7  # Friday is the 4th day of the week (0-based)
    return today + timedelta(days=days_until_friday)

def default_till_date():
    # return timezone.now() + timedelta(days=(7 - timezone.now().weekday()) % 7 + 7)
    return timezone.now() + timedelta(days=(0 - timezone.now().weekday()) % 7)


class WeeklyReport(models.Model):
    fr_dt = models.DateTimeField("From", default=timezone.now)
    to_dt = models.DateTimeField("Till", default=next_friday)
    paper_progress = models.TextField("Paper Progress")
    paper_prog_percent = models.IntegerField("Paper Progress Percent")
    paper_last_wk = models.TextField("Last Week Paper")
    paper_this_wk = models.TextField("This Week Paper")
    project_progress = models.TextField("Project Progress")
    project_prog_percent = models.IntegerField("Paper Progress Percent")
    project_last_wk = models.TextField("Last Week Project")
    project_this_wk = models.TextField("This Week Project")
    mnth_gls = models.TextField("Monthly Goals")
    annl_gls = models.TextField("Annual Goals")
    user = models.CharField(null=True, blank=True)
    writer = models.ForeignKey(Member, on_delete=models.DO_NOTHING, related_name='reports', default=get_default_user)
    # is_post_doc = models.BooleanField("Post Doc?",default=False)


class PostDocReport(models.Model):
    fr_dt = models.DateTimeField("From Date", default=timezone.now)
    to_dt = models.DateTimeField("Till", default=next_friday)
    paper_progress = models.TextField("Paper Progress")
    project_progress = models.TextField("Project Progress")
    mnth_gls = models.TextField("Monthly Goals")
    annl_gls = models.TextField("Annual Goals")
    user = models.CharField(null=True, blank=True)
    writer = models.ForeignKey(Member, on_delete=models.DO_NOTHING, related_name='post_doc_reports', default=get_default_user)


class Seminar(models.Model):
    visit = models.IntegerField(default=1, null=False, blank=True)
    write_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=150, null=True, blank=True)
    writer = models.ForeignKey(Member, on_delete=models.DO_NOTHING, related_name='seminar', default=get_default_user)
    file1 = models.FileField(upload_to='seminar/', null=True, blank=True)
    file2 = models.FileField(upload_to='seminar/', null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=False)
    ref = models.CharField(max_length=150, null=False, blank=True)
    tcp_ip = models.CharField(max_length=150, null=False, blank=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    subject = models.CharField(max_length=250)
    content = models.TextField()
    write_date = models.DateTimeField(default=timezone.now, null=True)
    update_date = models.DateTimeField(default=timezone.now, null=True)
    tcp_ip = models.CharField(max_length=150, null=False, blank=True)
    writer = models.ForeignKey(Member, on_delete=models.DO_NOTHING, related_name='review', default=get_default_user)
    

    def __str__(self):
        return self.subject

class PaperTemplate(models.Model):
    subject = models.CharField(max_length=250)
    content = models.TextField()
    write_date = models.DateTimeField(default=timezone.now, null=True)
    update_date = models.DateTimeField(default=timezone.now, null=True)
    tcp_ip = models.CharField(max_length=150, null=False, blank=True)
    writer = models.ForeignKey(Member, on_delete=models.DO_NOTHING, related_name='paper_templates', default=get_default_user)
    file1 = models.FileField(upload_to='paper_templates/', null=True, blank=True)
    file2 = models.FileField(upload_to='paper_templates/', null=True, blank=True)
    
    def __str__(self):
        return self.subject
