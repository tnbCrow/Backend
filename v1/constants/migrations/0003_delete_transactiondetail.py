# Generated by Django 3.1.6 on 2021-03-10 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('constants', '0002_auto_20210310_0924'),
        ('trades', '0004_auto_20210310_0924'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TransactionDetail',
        ),
    ]
