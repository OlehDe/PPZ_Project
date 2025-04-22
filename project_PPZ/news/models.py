from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    content = models.TextField("Текст")
    image = models.ImageField("Ілюстрація", upload_to='news_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name='news_articles')
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новина"
        verbose_name_plural = "Новини"
        ordering = ['-created_at']


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments', verbose_name="Новина")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name='news_comments')
    text = models.TextField("Текст коментаря")
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)

    def __str__(self):
        return f'Коментар від {self.author.username}'

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"
        ordering = ['created_at']
