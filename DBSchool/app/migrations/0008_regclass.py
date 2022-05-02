# Generated by Django 4.0.3 on 2022-04-15 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0007_rename_classid_quiz_classid'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.class')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
