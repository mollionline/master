# Generated by Django 4.0.1 on 2022-01-23 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='task',
            name='type',
        ),
        migrations.AddField(
            model_name='task',
            name='type',
            field=models.ManyToManyField(blank=True, related_name='tasks', through='issue_tracker.TaskType', to='issue_tracker.Type'),
        ),
        migrations.AddField(
            model_name='tasktype',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_type', to='issue_tracker.task', verbose_name='Задача'),
        ),
        migrations.AddField(
            model_name='tasktype',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_task', to='issue_tracker.type', verbose_name='Тип задачи'),
        ),
    ]
