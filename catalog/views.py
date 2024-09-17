from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView, TemplateView
from .forms import ProductForm, VersionForm
from .models import Product, Version

# Список продуктов
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

# Детали продукта
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

# Создание продукта
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

# Обновление продукта
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

# Удаление продукта
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

# Создание версии продукта
class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    template_name = 'version_form.html'
    success_url = reverse_lazy('catalog:home')

# Обновление версии продукта
class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    template_name = 'version_form.html'
    success_url = reverse_lazy('catalog:home')

# Удаление версии продукта
class VersionDeleteView(DeleteView):
    model = Version
    template_name = 'version_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

# О нас
class AboutView(TemplateView):
    template_name = 'about.html'

# Контакты
class ContactsView(TemplateView):
    template_name = 'contacts.html'
