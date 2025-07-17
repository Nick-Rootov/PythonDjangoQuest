from django.db import models

class Citation(models.Model):
    title = models.TextField('Цитата', max_length=1000)
    likes = models.DecimalField('Кол-во лайков',max_digits=9, decimal_places=0, default=0)
    weight = models.PositiveBigIntegerField('Вес', default=1)
    film = models.CharField('Фильм', max_length=50)

    def __str__(self):
        return self.title
class Like(models.Model):
    post = models.ForeignKey(Citation, on_delete=models.CASCADE)
    user = models.ForeignKey(on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['post', 'user'], ['post', 'session_key']]