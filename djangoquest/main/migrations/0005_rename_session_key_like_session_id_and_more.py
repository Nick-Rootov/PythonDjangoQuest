# Generated by Django 5.2.4 on 2025-07-18 17:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_like'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='session_key',
            new_name='session_id',
        ),
        migrations.RemoveField(
            model_name='citation',
            name='likes',
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('cit', 'session_id'), ('cit', 'user')},
        ),
        migrations.AlterField(
            model_name='like',
            name='cit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='main.citation'),
        ),
        migrations.RemoveField(
            model_name='like',
            name='created_time',
        ),
    ]
