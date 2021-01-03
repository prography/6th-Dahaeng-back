# Generated by Django 3.0.5 on 2020-12-30 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_firebaseuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firebaseuid',
            name='uid',
            field=models.CharField(max_length=300, unique=True, verbose_name='유저 UID (Firebase 에서 자동 생성)'),
        ),
    ]