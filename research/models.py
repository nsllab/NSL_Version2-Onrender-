from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from members.models import Member
from django import forms

from django.utils.text import slugify
from .choices import PROJECTS

# Create your models here.

def get_default_user():
    return get_user_model().objects.get(username='admin').id



class BaseProject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Project(models.Model):
    base_project = models.ForeignKey(BaseProject, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name

class History(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=255)
    write_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True, null=True)
    content = models.TextField()
    tcp_ip = models.CharField(max_length=20, null=True, blank=True)
    visit = models.IntegerField(default=1, null=True, blank=True)
    file1 = models.FileField(upload_to='projects/', null=True, blank=True)
    file2 = models.FileField(upload_to='projects/', null=True, blank=True)
    writer = models.ForeignKey(Member, on_delete=models.DO_NOTHING, default=get_default_user, related_name="project_history")
    
    def __str__(self):
        return self.subject

class UserInputForm(forms.Form):
    title = forms.CharField(max_length=255)
    text_content = forms.CharField(widget=forms.Textarea, required=False)
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)