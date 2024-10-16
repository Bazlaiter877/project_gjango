from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Наименование",
        help_text="Введите наименование категории",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Введите описание категории",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Наименование",
        help_text="Введите наименование продукта",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Введите описание продукта",
    )
    image = models.ImageField(
        upload_to="product_images/",
        blank=True,
        null=True,
        verbose_name="Изображение (превью)",
        help_text="Загрузите изображение продукта",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
        help_text="Выберите категорию для продукта",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за покупку",
        help_text="Введите цену продукта",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Владелец",
        help_text="Пользователь, создавший продукт",
    )

    # Новое поле для статуса публикации
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликован",
        help_text="Отметьте, если продукт опубликован"
    )

    def __str__(self):
        return self.name

    def current_version(self):
        """Возвращает текущую версию продукта."""
        return self.versions.filter(is_current=True).first()

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["-created_at"]

        # Новые права доступа для модераторов
        permissions = [
            ("can_unpublish_product", "Может отменить публикацию продукта"),
            ("can_edit_description", "Может изменять описание продукта"),
            ("can_edit_category", "Может изменять категорию продукта"),
        ]


class BlogPost(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.CharField(max_length=255, unique=True, verbose_name="Slug")
    content = models.TextField(verbose_name="Содержимое")
    preview_image = models.ImageField(
        upload_to="blog_previews/",
        blank=True,
        null=True,
        verbose_name="Превью",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    class Meta:
        verbose_name = "Блоговая запись"
        verbose_name_plural = "Блоговые записи"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})


class Version(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="versions",
        verbose_name="Продукт",
    )
    version_number = models.CharField(max_length=10, verbose_name="Номер версии")
    version_name = models.CharField(max_length=255, verbose_name="Название версии")
    is_current = models.BooleanField(default=False, verbose_name="Текущая версия")

    def save(self, *args, **kwargs):
        if self.is_current:
            Version.objects.filter(product=self.product, is_current=True).update(is_current=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.version_name} ({self.version_number})"

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
