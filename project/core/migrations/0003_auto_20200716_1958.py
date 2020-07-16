# Generated by Django 3.0.5 on 2020-07-16 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_profile_social'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(blank=True, choices=[('0', '일반 유저'), ('10', '관리자')], default='0', max_length=2),
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, choices=[('0', '가입대기'), ('1', '가입활성화'), ('8', '블랙리스트'), ('9', '탈퇴')], default='1', max_length=2),
        ),
    ]