from django.contrib.auth.mixins import LoginRequiredMixin
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
        form.instance.owner = self.request.user
        return super().form_valid(form)


# Обновление продукта
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:product_list')


# Удаление продукта
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')


# Создание версии продукта
class VersionCreateView(LoginRequiredMixin, CreateView):
    model = Version
    form_class = VersionForm
    template_name = 'catalog/version_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['product_id'] = self.kwargs.get('product_id')
        return kwargs

    def form_valid(self, form):
        form.instance.product_id = self.kwargs.get('product_id')
        return super().form_valid(form)


# Обновление версии продукта
class VersionUpdateView(LoginRequiredMixin, UpdateView):
    model = Version
    form_class = VersionForm
    template_name = 'catalog/version_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.product.pk})


# Удаление версии продукта
class VersionDeleteView(LoginRequiredMixin, DeleteView):
    model = Version
    template_name = 'catalog/version_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.product.pk})


# О нас
class AboutView(TemplateView):
    template_name = 'about.html'


# Контакты
class ContactsView(TemplateView):
    template_name = 'contacts.html'
