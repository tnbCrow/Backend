# Generated by Django 3.1.6 on 2021-03-10 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20210310_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='memo',
            field=models.CharField(default='tnbcrow-<function uuid4 at 0x0350F978>', editable=False, max_length=44, unique=True),
        ),
    ]