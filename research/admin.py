from django.contrib import admin
from .models import Project, History, BaseProject

# Register your models here.
admin.site.register(BaseProject)
admin.site.register(Project)
admin.site.register(History)
