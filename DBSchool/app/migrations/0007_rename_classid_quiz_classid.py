# Generated by Django 4.0.3 on 2022-04-15 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_addclass_class_quiz_classid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='Classid',
            new_name='classid',
        ),
    ]
