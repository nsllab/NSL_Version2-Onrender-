# Generated by Django 4.2.9 on 2024-01-15 04:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeklyreport',
            name='fr_dt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]