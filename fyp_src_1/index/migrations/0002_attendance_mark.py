# Generated by Django 3.1.8 on 2023-02-02 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='Mark',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
