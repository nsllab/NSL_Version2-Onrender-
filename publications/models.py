from django.db import models


# from accounts.models import CustomUser
from django.utils import timezone
from django.contrib.auth import get_user_model
from .choices import PAPER_STATUS, PAPER_TYPE
from members.models import Member

def get_default_user():
    return get_user_model().objects.get(username='admin').id

# Create your models here.
class Journal(models.Model):
    title = models.CharField(max_length=500, null=True, blank=False)
    journal_name = models.CharField(max_length=100, null=True)
    abstract = models.TextField(null=True)
    status = models.IntegerField(choices=PAPER_STATUS, default=1, null=True)
    journal_type = models.IntegerField(choices=PAPER_TYPE, default=1, null=True)
    # writer = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='journals', default=get_default_user)
    writer = models.ForeignKey(Member, on_delete=models.DO_NOTHING, related_name='journals', default=get_default_user)
    write_date = models.DateTimeField(default=timezone.now, null=True)
    update_date = models.DateTimeField(default=timezone.now, null=True)
    visit = models.IntegerField(default=1)
    ack = models.CharField(max_length=100, null=True, blank=True)
    pub_year = models.CharField(max_length=10, blank=True, null=True)
    # extras = models.CharField(max_length=50, null=True, blank=True)
    all_authors = models.CharField(max_length=500, null=True, blank=True)
    file = models.FileField(upload_to='journals/', null=True, blank=True)
    cite = models.CharField(max_length=300, null=False, blank=True)

    def __str__(self):
        return self.title


class Conference(models.Model):
    title = models.CharField(max_length=500, null=True, blank=False)
    conference_name = models.CharField(max_length=100, null=True)
    abstract = models.TextField(null=True)
    status = models.IntegerField(choices=PAPER_STATUS, default=1, null=True)
    conference_type = models.IntegerField(choices=PAPER_TYPE, default=1, null=True)
    # # writer = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='journals', default=get_default_user)
    writer = models.ForeignKey(Member, on_delete=models.DO_NOTHING, related_name='conferences', default=get_default_user)
    write_date = models.DateTimeField(default=timezone.now, null=True)
    update_date = models.DateTimeField(default=timezone.now, null=True)
    visit = models.IntegerField(default=1)
    ack = models.CharField(max_length=100, null=True, blank=True)
    pub_year = models.CharField(max_length=10, blank=True, null=True)
    # extras = models.CharField(max_length=50, null=True, blank=True)
    all_authors = models.CharField(max_length=500, null=True, blank=True)
    cite = models.CharField(max_length=300, null=False, blank=True)
    file = models.FileField(upload_to='conference/', null=True, blank=True)

    def __str__(self):
        return self.title


class Patent(models.Model):
    subject = models.CharField(max_length=150, null=False)
    content = models.TextField()
    status = models.IntegerField(null=True)
    write_date = models.DateTimeField(default=timezone.now, null=True)
    update_date = models.DateTimeField(default=timezone.now, null=True)
    ref = models.CharField(max_length=100, null=True, blank=True)
    writer = models.CharField(max_length=100, null=False)
    visit = models.IntegerField(default=1)
    tcp_ip = models.CharField(max_length=100, null=True)
    patent_type = models.IntegerField(choices=PAPER_TYPE, default=1, null=True)

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=500, null=True, blank=False)
    ref = models.CharField(max_length=100, null=False, blank=True)
    abstract = models.TextField(null=False, blank=True)
    visit = models.IntegerField(default=1, null=False, blank=True)
    write_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)
    writer = models.ForeignKey(Member, on_delete=models.DO_NOTHING, related_name='books', default=get_default_user)
    file1 = models.FileField(upload_to='books/', null=True, blank=True)
    file2 = models.FileField(upload_to='books/', null=True, blank=True)

    def __str__(self):
        return self.title