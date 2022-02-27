from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    profile = models.CharField(null=True, blank=True, max_length=100, verbose_name='Профиль')
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Аватар')
    about_profile = models.TextField(null=True, blank=True, max_length=1000, verbose_name='О себе')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"
