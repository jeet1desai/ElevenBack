# Generated by Django 5.0.4 on 2024-04-20 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_membership_modified_by_membership_modified_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Collaborator'), (2, 'Power Collaborator'), (3, 'Admin'), (4, 'Super Admin')], default=1),
        ),
    ]
