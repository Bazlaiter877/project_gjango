from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView, TemplateView
from .forms import ProductForm, VersionForm
from .models import Product, Version


# Список продуктов
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'


# Детали продукта
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    current_version = product.current_version()
    versions = product.versions.all()
    return render(request, 'product_detail.html', {
        'product': product,
        'current_version': current_version,
        'versions': versions,
    })


# Создание продукта
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Привязка продукта к текущему пользователю
        return super().form_valid(form)


# Обновление продукта
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        """Проверка, что текущий пользователь является владельцем продукта"""
        product = self.get_object()
        return self.request.user == product.owner

    def handle_no_permission(self):
        return render(self.request, '403.html')  # Страница 403 при отсутствии доступа


# Удаление продукта
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        """Проверка, что текущий пользователь является владельцем продукта"""
        product = self.get_object()
        return self.request.user == product.owner

    def handle_no_permission(self):
        return render(self.request, '403.html')  # Страница 403 при отсутствии доступа


# Создание версии продукта
class VersionCreateView(LoginRequiredMixin, CreateView):
    model = Version
    form_class = VersionForm
    template_name = 'catalog/version_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_form_kwargs(self):
        """Передаем product_id в форму для привязки версии к продукту"""
        kwargs = super().get_form_kwargs()
        kwargs['product_id'] = self.kwargs.get('product_id')
        return kwargs

    def form_valid(self, form):
        """Привязка версии к продукту"""
        form.instance.product_id = self.kwargs.get('product_id')
        return super().form_valid(form)


# Обновление версии продукта
class VersionUpdateView(LoginRequiredMixin, UpdateView):
    model = Version
    form_class = VersionForm
    template_name = 'catalog/version_form.html'

    def get_success_url(self):
        """Перенаправление на страницу продукта после обновления версии"""
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.product.pk})


# Удаление версии продукта
class VersionDeleteView(LoginRequiredMixin, DeleteView):
    model = Version
    template_name = 'catalog/version_confirm_delete.html'

    def get_success_url(self):
        """Перенаправление на страницу продукта после удаления версии"""
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.product.pk})


# О нас
class AboutView(TemplateView):
    template_name = 'about.html'


# Контакты
class ContactsView(TemplateView):
    template_name = 'contacts.html'
