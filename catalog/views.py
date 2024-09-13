from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView, TemplateView
from django import forms
from .models import Product

# Запрещенные слова для проверки
FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

# Валидация для полей формы продукта
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

    # Валидация названия
    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        for word in FORBIDDEN_WORDS:
            if word in name.lower():
                raise forms.ValidationError(f"Запрещено использовать слово '{word}' в названии продукта.")
        return name

    # Валидация описания
    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        for word in FORBIDDEN_WORDS:
            if word in description.lower():
                raise forms.ValidationError(f"Запрещено использовать слово '{word}' в описании продукта.")
        return description

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
    success_url = reverse_lazy('catalog:home')  # Исправлено на 'catalog:home'

# Обновление продукта
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')  # Исправлено на 'catalog:home'

# Удаление продукта
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')  # Исправлено на 'catalog:home'

# О нас
class AboutView(TemplateView):
    template_name = 'about.html'

# Контакты
class ContactsView(TemplateView):
    template_name = 'contacts.html'
