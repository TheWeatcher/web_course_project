"""
Definition of models.
"""

from django.db import models


# Create your models here.
from datetime import datetime
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User





class Blog(models.Model):
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    description = models.TextField(verbose_name = "Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликован")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")

    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

class Comment(models.Model):
    text = models.TextField(verbose_name = "Комментарий")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор")
    post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Новость")

    def __str__(self):
        return 'Комментарий %s к %s' % (self.author, self.post)

    class Meta:
        db_table = "Comments"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарий к новости"
        ordering = ["-date"]

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name = "Жанр")
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name = "Слаг")
 
    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
 
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('app:game_list_by_category', args=[self.slug])
 
class Game(models.Model):
    category = models.ForeignKey(Category, related_name='games', verbose_name = "Жанр")
    name = models.CharField(max_length=200, db_index=True, verbose_name = "Название")
    slug = models.SlugField(max_length=200, db_index=True, verbose_name = "Слаг")
    image = models.ImageField(upload_to='games/%Y/%m/%d', blank=True, verbose_name = "Изображение")
    description = models.TextField(blank=True, verbose_name = "Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name = "Цена")
    stock = models.PositiveIntegerField(verbose_name = "Количество")
    available = models.BooleanField(default=True, verbose_name = "Доступнен")
    created = models.DateTimeField(auto_now_add=True, verbose_name = "Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name = "Обновлен")
 
    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
 
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('app:game_detail', args=[self.id, self.slug])


admin.site.register(Blog)
admin.site.register(Comment)