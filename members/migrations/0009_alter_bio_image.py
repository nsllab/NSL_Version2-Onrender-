# Generated by Django 4.2.9 on 2024-01-16 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_remove_bio_last_name_alter_bio_email_list_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bio',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]