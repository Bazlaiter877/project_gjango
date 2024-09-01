from django.db import models
from django.utils.text import slugify

class BlogPost(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
        help_text="Введите заголовок статьи",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name="Slug",
        help_text="Уникальный URL для статьи",
    )
    content = models.TextField(
        verbose_name="Содержимое",
        help_text="Введите содержимое статьи",
    )
    preview_image = models.ImageField(
        upload_to="blog_images/",
        blank=True,
        null=True,
        verbose_name="Изображение (превью)",
        help_text="Загрузите изображение для статьи",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата создания статьи",
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликована",
        help_text="Опубликовать статью",
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество просмотров",
        help_text="Количество просмотров статьи",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Блоговая статья"
        verbose_name_plural = "Блоговые статьи"
        ordering = ["-created_at"]
