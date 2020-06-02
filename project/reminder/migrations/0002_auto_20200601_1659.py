# Generated by Django 3.0.5 on 2020-06-01 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reminder',
            name='is_sent',
        ),
        migrations.AddField(
            model_name='reminder',
            name='interval',
            field=models.IntegerField(default=7),
            preserve_default=False,
        ),
    ]
