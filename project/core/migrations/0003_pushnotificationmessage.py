# Generated by Django 3.0.5 on 2020-11-19 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_userfeedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='PushNotificationMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('h', 'happy word'), ('r', 'reminder word')], default='h', max_length=2)),
            ],
        ),
    ]
