from django.core.cache import cache
from .models import Category, Product  # замените на вашу модель категории
from django.conf import settings


def get_cached_categories():
    """
    Возвращает закешированный список категорий. Если данных нет в кеше,
    выполняет запрос к базе данных и сохраняет результат в кеше.
    """
    categories = cache.get('categories_list')
    if categories is None:
        categories = list(Category.objects.all())
        cache.set('categories_list', categories, timeout=3600)  # Кешируем на 1 час
    return categories


def get_cached_products():
    """
    Возвращает закешированный список продуктов. Если данных нет в кеше,
    выполняет запрос к базе данных и сохраняет результат в кеше.
    """
    products = cache.get('products_list')
    if products is None:
        products = list(Product.objects.all())
        cache.set('products_list', products, timeout=3600)  # Кешируем на 1 час
    return products
