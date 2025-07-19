from django.db import models
from django.contrib.auth.models import User

class Citation(models.Model):
    title = models.TextField('Цитата', max_length=1000)
    #likes = models.DecimalField('Кол-во лайков',max_digits=9, decimal_places=0, default=0)
    weight = models.PositiveBigIntegerField('Вес', default=1)
    film = models.CharField('Фильм', max_length=50)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    @property
    def total_likes(self):
        return self.likes.count()

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

class Like(models.Model):
    cit = models.ForeignKey(
        Citation,
        related_name='likes',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    session_id = models.CharField(
        max_length=40,
        null=True,
        blank=True
    )

    class Meta:
        # Гарантируем уникальность один пользователь/сессия - один лайк на пост
        unique_together = [['cit', 'user'], ['cit', 'session_id']]