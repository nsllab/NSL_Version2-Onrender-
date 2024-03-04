from django.db import models
from django.contrib.auth.models import AbstractUser
# from hello_django.storage_backends import PublicMediaStorage, PrivateMediaStorage
from publications.choices import POSITION
from django.core.files.storage import default_storage
# from cloudinary_storage.storage import MediaCloudinaryStorage
# import

# Create your models here.

class Member(AbstractUser):
    # address = models.CharField(max_length=150, null=True, blank=True)
    login_cnt = models.IntegerField(default=0) # increments
    restriction_date = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

# Create your models here.

class Bio(models.Model):
    name = models.CharField('Full Name', max_length=255)
    # last_name = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    research_area = models.CharField()
    education = models.TextField()
    career = models.TextField(null=True, blank=True)
    position = models.IntegerField(choices=POSITION, default=1, null=False, blank=False)
    display_order = models.IntegerField()
    link = models.URLField(blank=True, null=True)
    email_list = models.CharField('Email')
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         old_instance = Bio.objects.get(pk=self.pk)
    #         if old_instance.image:
    #             default_storage.delete(old_instance.image.name)
    #     super().save(*args, **kwargs)

    # date_joined 
    # user = models.OneToOneField(Member, on_delete=models.DO_NOTHING, related_name='bio', null=True, blank=True)


    # def get_fullname(self):
    #     return f"{self.name} {self.last_name}"
    # def __str__(self):
    #     return self.name