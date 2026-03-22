from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')

    # Связь многие-ко-многим через промежуточную модель Scope
    tags = models.ManyToManyField(Tag, through='Scope', related_name='articles')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Scope(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes')
    is_main = models.BooleanField(default=False, verbose_name='Основной')

    class Meta:
        verbose_name = 'Связь статьи и раздела'
        verbose_name_plural = 'Связи статей и разделов'
        # Ограничение: у статьи может быть только один основной раздел
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'is_main'],
                condition=models.Q(is_main=True),
                name='unique_main_scope_per_article'
            )
        ]

    def __str__(self):
        return f"{self.article.title} - {self.tag.name} (Основной: {self.is_main})"