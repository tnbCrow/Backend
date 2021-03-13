# Generated by Django 3.1.6 on 2021-03-07 08:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trades', '0004_auto_20210306_2146'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activetrade',
            old_name='initiator_accepted',
            new_name='initiator_confirmed',
        ),
        migrations.RenameField(
            model_name='activetrade',
            old_name='owner_accepted',
            new_name='owner_confirmed',
        ),
        migrations.CreateModel(
            name='CompletedTrade',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]