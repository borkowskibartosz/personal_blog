# Generated by Django 3.1 on 2020-08-22 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20200820_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='reset_password',
            field=models.BooleanField(default=False),
        ),
    ]
