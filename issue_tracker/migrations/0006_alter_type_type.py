# Generated by Django 4.0.1 on 2022-01-24 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker', '0005_rename_type_new_task_type_remove_task_type_old_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='type',
            name='type',
            field=models.CharField(max_length=50),
        ),
    ]
