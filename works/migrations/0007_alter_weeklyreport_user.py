# Generated by Django 4.2.9 on 2024-01-15 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0006_weeklyreport_writer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeklyreport',
            name='user',
            field=models.CharField(blank=True, default=None, null=True),
        ),
    ]