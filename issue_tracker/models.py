from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import get_candidate_relations_to_delete

from issue_tracker.validators import MinLengthValidator


class CustomModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


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
    summary = models.CharField(
        max_length=50, null=False, blank=False,
        validators=(MinLengthValidator(5),)
    )
    description = models.TextField(max_length=1000, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_deleted = models.BooleanField(default=False)
    objects = CustomModelManager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save(update_fields=['is_deleted', ])

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


class Project(models.Model):
    project = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=False)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    objects = CustomModelManager()
    user = models.ManyToManyField(
        get_user_model(), related_name='projects',
        verbose_name='Пользователь'
    )

    def delete(self, using=None, keep_parents=False):  # noqa C901
        self.is_deleted = True
        delete_candidates = get_candidate_relations_to_delete(self.__class__._meta)
        if delete_candidates:
            for rel in delete_candidates:
                if rel.on_delete.__name__ == 'CASCADE' and rel.one_to_many and not rel.hidden:
                    for item in getattr(self, rel.related_name).all():
                        item.delete()
        self.save(update_fields=['is_deleted', ])

    def __str__(self):
        return f'{self.project}'
