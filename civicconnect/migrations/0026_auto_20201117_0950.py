# Generated by Django 3.1.1 on 2020-11-17 14:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('civicconnect', '0025_auto_20201108_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 17, 9, 50, 46, 139476)),
        ),
    ]
