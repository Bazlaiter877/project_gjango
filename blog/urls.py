from django.urls import path
from .views import (
    BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView,
    ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView
)

app_name = 'blog'

urlpatterns = [
    # BlogPost URLs
    path('', BlogPostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', BlogPostDetailView.as_view(), name='post_detail'),
    path('post/create/', BlogPostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/update/', BlogPostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='post_delete'),

    # Product URLs
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
