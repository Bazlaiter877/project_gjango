from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from .models import Product, Version


# Миксин для стилизации форм
class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        # Настройка FormHelper для стилизации
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'  # Пример, можно изменить по своему усмотрению


# Запрещённые слова для проверки
FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


# Форма для продукта
class ProductForm(forms.ModelForm, FormControlMixin):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Введите описание'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите цену'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_forbidden_words(self, field_value, field_name):
        """Проверка наличия запрещённых слов в поле."""
        if any(word in field_value.lower() for word in FORBIDDEN_WORDS):
            raise forms.ValidationError(f"Запрещено использовать слово '{field_value}' в {field_name}.")
        return field_value

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        return self.clean_forbidden_words(name, 'название продукта')

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        return self.clean_forbidden_words(description, 'описание продукта')


# Форма для версий продукта
class VersionForm(forms.ModelForm, FormControlMixin):
    class Meta:
        model = Version
        fields = ['version_number', 'version_name', 'is_current']

    def __init__(self, *args, **kwargs):
        self.product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('version_number'),
            Field('version_name'),
            Field('is_current'),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn btn-primary')
            )
        )
