# Generated by Django 4.1.3 on 2023-02-01 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_alter_employee_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='Present',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='InTime',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='OutTime',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterModelTable(
            name='attendance',
            table='Attendance',
        ),
    ]