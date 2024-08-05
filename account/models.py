from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


genders = [("M", 'Male'), ("F", 'Female')]


class Profile(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', verbose_name="Аватарка")
    phone_num = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона')
    bio = models.CharField(max_length=70, blank=True, null=True, verbose_name='Информация о пользователе')
    gender = models.CharField(choices=genders, blank=True, null=True)
    posts_count = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)

    followers = models.ManyToManyField('self', through='Subscription', symmetrical=False, related_name='following')

    groups = models.ManyToManyField('auth.Group', related_name='profile_user_set', blank=True, verbose_name='groups')
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='profile_user_set', blank=True, verbose_name='user permissions')

    def __str__(self):
        return self.username


class Subscription(models.Model):
    follower = models.ForeignKey(Profile, related_name='follower_set', on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, related_name='following_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

