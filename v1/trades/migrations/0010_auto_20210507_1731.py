# Generated by Django 3.1.7 on 2021-05-07 11:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0009_auto_20210507_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traderequest',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 8, 11, 46, 7, 537288, tzinfo=utc)),
        ),
    ]