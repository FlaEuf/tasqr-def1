# Generated by Django 3.0.8 on 2020-09-19 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20200810_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='codice',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='socialcodice',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
