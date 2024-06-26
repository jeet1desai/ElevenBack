# Generated by Django 5.0.4 on 2024-05-02 18:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_url_task_urls'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='urls',
        ),
        migrations.CreateModel(
            name='TaskURL',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=500)),
                ('is_active', models.BooleanField(default=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urls', to='tasks.task')),
            ],
        ),
        migrations.DeleteModel(
            name='URL',
        ),
    ]
