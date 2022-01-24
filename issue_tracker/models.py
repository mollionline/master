from django.db import models


# Create your models here.
class Status(models.Model):
    status = models.CharField(max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return '{}'.format(self.status)


class Type(models.Model):
    type = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.type)


class Task(models.Model):
    summary = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(max_length=1000, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)

    type = models.ManyToManyField(
        'issue_tracker.Type',
        related_name='tasks',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    def __str__(self):
        return '{}. {}'.format(self.pk, self.summary)
