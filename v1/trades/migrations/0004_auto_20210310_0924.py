# Generated by Django 3.1.6 on 2021-03-10 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('constants', '0002_auto_20210310_0924'),
        ('trades', '0003_tradepost_transaction_detail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tradepost',
            name='transaction_detail',
        ),
        migrations.AddField(
            model_name='tradepost',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='constants.currency'),
            preserve_default=False,
        ),
    ]