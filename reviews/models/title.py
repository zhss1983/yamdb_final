from django.db import models

from .category import Category
from .genre import Genre
from .validators import year_validator


class Title(models.Model):
    name = models.CharField(verbose_name="Произведение", max_length=200, db_index=True)
    year = models.IntegerField(
        verbose_name="Год публикации",
        blank=False,
        db_index=True,
        validators=(year_validator,),
    )
    genre = models.ManyToManyField(Genre, verbose_name="Жанр")
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.PROTECT,
        related_name="titles",
    )
    description = models.TextField("Описание")

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name
