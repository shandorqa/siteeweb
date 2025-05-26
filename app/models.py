"""
Definition of models.
"""

from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок", blank=True, null=True)
    description = models.TextField(verbose_name="Краткое содержание", blank=True, null=True)
    content = models.TextField(verbose_name="Полное содержание", blank=True, null=True)
    posted = models.DateTimeField(default = timezone.now, db_index = True, verbose_name = "Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")
    
    def get_absolute_url(self):
        return reverse('blogpost', args=[str(self.id)])
    
    def __str__(self):
        return self.title or "Без заголовка"

class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Комментарий от {self.author} к {self.post}'

admin.site.register(Blog)
admin.site.register(Comment)
