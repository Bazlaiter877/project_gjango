from django.views.generic import ListView, DetailView, TemplateView
from .models import Product


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactsView(TemplateView):
    template_name = 'contacts.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
