from django.db import models


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=256, unique=True)
    slug = models.SlugField('Адрес жанра', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name
