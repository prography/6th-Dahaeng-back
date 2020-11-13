# Generated by Django 3.0.5 on 2020-11-13 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import record.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateField(auto_now=True)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='record.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('emotion', models.CharField(choices=[('WARM', '따뜻했어요'), ('FUN', '즐거웠어요'), ('HAPPY', '기뻤어요'), ('TOUCHED', '감동이에요'), ('EXTRA', '기타')], default='WARM', max_length=10)),
                ('detail', models.TextField(blank=True)),
                ('image', models.ImageField(null=True, upload_to=record.models.date_upload_to)),
                ('continuity', models.IntegerField(default=0)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='record.Question')),
            ],
            options={
                'ordering': ('-created_at',),
                'unique_together': {('created_at', 'profile')},
            },
        ),
    ]
