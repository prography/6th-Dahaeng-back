# Generated by Django 3.0.5 on 2020-10-09 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jorang',
            name='status',
            field=models.CharField(choices=[('0', '알'), ('1', '유년기'), ('2', '성장기')], default=0, max_length=2),
        ),
    ]
