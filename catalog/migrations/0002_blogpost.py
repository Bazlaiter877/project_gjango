# Generated by Django 5.0.7 on 2024-09-01 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Заголовок")),
                (
                    "slug",
                    models.CharField(max_length=255, unique=True, verbose_name="Slug"),
                ),
                ("content", models.TextField(verbose_name="Содержимое")),
                (
                    "preview_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="blog_previews/",
                        verbose_name="Превью",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(default=False, verbose_name="Опубликовано"),
                ),
                (
                    "views_count",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Количество просмотров"
                    ),
                ),
            ],
            options={
                "verbose_name": "Блоговая запись",
                "verbose_name_plural": "Блоговые записи",
                "ordering": ["-created_at"],
            },
        ),
    ]