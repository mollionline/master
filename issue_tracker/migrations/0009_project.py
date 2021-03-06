# Generated by Django 4.0.1 on 2022-02-06 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker', '0008_alter_task_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('project', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
