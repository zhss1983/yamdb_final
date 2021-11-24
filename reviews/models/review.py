from django.db import models

from api.users.models import User

from .title import Title


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.PROTECT,
        related_name='reviews'
    )
    text = models.TextField('Отзыв')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField('Оценка', default=5, blank=False)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date', )
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_title_author',
            ),
            models.CheckConstraint(
                check=models.Q(score__gte=1),
                name='score_gte_1',
            ),
            models.CheckConstraint(
                check=models.Q(score__lte=10),
                name='score_lte_10',
            )
        )

    def __str__(self):
        return self.text[:15]
