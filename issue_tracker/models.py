from django.db import models
from issue_tracker.validators import MinLengthValidator


# Create your models here.
class Entity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    class Meta:
        abstract = True


class Status(models.Model):
    status = models.CharField(max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return '{}'.format(self.status)


class Type(models.Model):
    type = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.type)


class Task(Entity):
    summary = models.CharField(max_length=50, null=False, blank=False, validators=(MinLengthValidator(5),))
    description = models.TextField(max_length=1000, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)

    type = models.ManyToManyField(
        'issue_tracker.Type',
        related_name='tasks',
        blank=False
    )

    project = models.ForeignKey(
        'issue_tracker.Project',
        related_name='tasks',
        on_delete=models.CASCADE,
        verbose_name='Проект',
        default=1
    )

    def __str__(self):
        return '{}. {}'.format(self.pk, self.summary)


class Project(Entity):
    project = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f'{self.project}'
