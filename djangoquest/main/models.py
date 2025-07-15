from django.db import models

class Citation(models.Model):
    title = models.TextField('Цитата', max_length=1000)
    likes = models.DecimalField('Кол-во лайков',max_digits=9, decimal_places=0, default=0)
    weight = models.PositiveBigIntegerField('Вес', default=1)
    film = models.CharField('Фильм', max_length=50)

    def __str__(self):
        return self.title
