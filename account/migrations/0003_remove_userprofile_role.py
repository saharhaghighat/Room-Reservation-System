# Generated by Django 5.0.2 on 2024-03-14 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='role',
        ),
    ]