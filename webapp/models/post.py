from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    image = models.ImageField(upload_to='post/', verbose_name='Изображение')
    summary = models.CharField(max_length=500, blank=True, verbose_name='Описание')
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.summary[:30]
