from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Comment(models.Model):
    comment = models.CharField(max_length=300, verbose_name="Комментарий")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='Пост', related_name='comment')
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    class Meta:
        db_table = "comment"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

