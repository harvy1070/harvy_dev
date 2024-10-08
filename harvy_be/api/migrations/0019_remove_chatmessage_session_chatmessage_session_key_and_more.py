# Generated by Django 5.1.1 on 2024-10-08 01:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_remove_chatmessage_is_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessage',
            name='session',
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='chatmessage',
            index=models.Index(fields=['user'], name='api_chatmes_user_id_ee15fd_idx'),
        ),
        migrations.AddIndex(
            model_name='chatmessage',
            index=models.Index(fields=['session_key'], name='api_chatmes_session_fe703c_idx'),
        ),
        migrations.AlterModelTable(
            name='chatmessage',
            table=None,
        ),
    ]
