# Generated by Django 3.1 on 2020-08-24 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0005_auto_20200815_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='botsettings',
            name='abort',
            field=models.BooleanField(default=False),
        ),
    ]
