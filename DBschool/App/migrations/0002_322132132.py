# Generated by Django 4.0.3 on 2022-04-12 05:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submit',
            name='UserName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='score',
            name='ProblemID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.problem'),
        ),
        migrations.AddField(
            model_name='score',
            name='StudentID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='regclass',
            name='ClassID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.class'),
        ),
        migrations.AddField(
            model_name='regclass',
            name='UserID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quiz',
            name='ClassID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.class'),
        ),
        migrations.AddField(
            model_name='problem',
            name='Query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.query'),
        ),
        migrations.AddField(
            model_name='class',
            name='Teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]