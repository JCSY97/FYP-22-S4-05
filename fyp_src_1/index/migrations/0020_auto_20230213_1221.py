# Generated by Django 3.1.8 on 2023-02-13 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0019_auto_20230212_1828'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workschedule',
            name='AttendanDate',
        ),
        migrations.RemoveField(
            model_name='workschedule',
            name='EndDate',
        ),
    ]
