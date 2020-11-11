import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150, null=True)
    publication_date = models.IntegerField(
        validators=[MinValueValidator(868), max_value_current_year], null=True
    )
    ISBN_number = models.CharField(max_length=30, null=True)
    number_of_pages = models.IntegerField(blank=True, null=True)
    link_to_cover = models.TextField(null=True)
    language = models.CharField(max_length=30, null=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
