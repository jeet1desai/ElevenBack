# Generated by Django 5.0.4 on 2024-05-02 20:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_membership_company'),
        ('tasks', '0003_remove_task_urls_taskurl_delete_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='project.project'),
        ),
    ]