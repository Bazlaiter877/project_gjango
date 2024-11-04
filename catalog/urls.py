from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home'),

    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', cache_page(900)(views.product_detail), name='product_detail'),  # Кешируем на 15 минут
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    path('product/<int:product_id>/version/create/', views.VersionCreateView.as_view(), name='version_create'),
    path('version/<int:pk>/update/', views.VersionUpdateView.as_view(), name='version_update'),
    path('version/<int:pk>/delete/', views.VersionDeleteView.as_view(), name='version_delete'),

    path('about/', views.AboutView.as_view(), name='about'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),

    path('categories/', views.CategoryListView.as_view(), name='category_list'),
]
