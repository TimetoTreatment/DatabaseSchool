# Generated by Django 4.0.3 on 2022-04-03 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_register_time',
        ),
    ]
