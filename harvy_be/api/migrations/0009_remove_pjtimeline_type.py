# Generated by Django 5.1.1 on 2024-09-16 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_userinfo_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pjtimeline',
            name='type',
        ),
    ]
