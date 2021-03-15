# Generated by Django 3.1.6 on 2021-03-10 03:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('constants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='transactiondetail',
            name='type',
        ),
    ]
