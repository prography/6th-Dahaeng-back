# Generated by Django 3.0.5 on 2020-07-16 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='social',
            field=models.CharField(blank=True, choices=[('KAKAO', 'kakao'), ('NAVER', 'naver'), ('APPLE', 'apple'), ('NONE', 'none')], default='NONE', max_length=20, null=True),
        ),
    ]