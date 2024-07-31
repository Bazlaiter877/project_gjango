import json
from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Fill the database with initial data from JSON file after clearing it"

    @staticmethod
    def json_read_categories():
        with open("fixtures/catalog_data.json", encoding="utf-8") as file:
            data = json.load(file)
            return [item for item in data if item["model"] == "catalog.category"]

    @staticmethod
    def json_read_products():
        with open("fixtures/catalog_data.json", encoding="utf-8") as file:
            data = json.load(file)
            return [item for item in data if item["model"] == "catalog.product"]

    def handle(self, *args, **options):
        # Удаляем все продукты и категории
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создаем списки для хранения объектов
        categories_for_create = []
        products_for_create = []

        # Обходим все значения категорий из фикстуры для получения информации об одном объекте
        for category_data in self.json_read_categories():
            fields = category_data["fields"]
            category = Category(id=category_data["pk"], **fields)
            categories_for_create.append(category)

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(categories_for_create)

        # Обходим все значения продуктов из фикстуры для получения информации об одном объекте
        for product_data in self.json_read_products():
            fields = product_data["fields"]
            fields["category"] = Category.objects.get(pk=fields["category"])
            product = Product(id=product_data["pk"], **fields)
            products_for_create.append(product)

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(products_for_create)

        self.stdout.write(
            self.style.SUCCESS("Database successfully seeded with initial data")
        )
