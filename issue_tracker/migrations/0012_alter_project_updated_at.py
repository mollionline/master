# Generated by Django 4.0.1 on 2022-02-07 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker', '0011_alter_project_created_at_alter_project_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
