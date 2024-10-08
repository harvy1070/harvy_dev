# Generated by Django 5.1.1 on 2024-10-09 10:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_remove_userpreference_user_id_userpreference_user_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='portfoliokeyword',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='portfoliokeyword',
            name='frequency',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='portfoliokeyword',
            name='keyword',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='portfoliokeyword',
            name='portfolio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='keywords', to='api.portfolioboard'),
        ),
        migrations.AlterUniqueTogether(
            name='portfoliokeyword',
            unique_together={('portfolio_name', 'keyword')},
        ),
    ]
