from django import forms
from .models import Product, Version


# Миксин для стилизации форм
class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Применяем класс 'form-control' ко всем полям формы
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


# Запрещённые слова для проверки
FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


# Форма для продукта
class ProductForm(forms.ModelForm, FormControlMixin):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

    def clean_forbidden_words(self, field_value, field_name):
        """Проверка наличия запрещённых слов в поле."""
        for word in FORBIDDEN_WORDS:
            if word in field_value.lower():
                raise forms.ValidationError(f"Запрещено использовать слово '{word}' в {field_name}.")
        return field_value

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        return self.clean_forbidden_words(name, 'названии продукта')

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        return self.clean_forbidden_words(description, 'описании продукта')


# Форма для версий продукта
class VersionForm(forms.ModelForm, FormControlMixin):
    class Meta:
        model = Version
        fields = ['version_number', 'version_name', 'is_current']

    def clean_version_number(self):
        version_number = self.cleaned_data.get('version_number', '')
        if not version_number.isalnum():
            raise forms.ValidationError("Номер версии должен содержать только буквы и цифры.")
        return version_number

    def clean_version_name(self):
        version_name = self.cleaned_data.get('version_name', '')
        if any(word in version_name.lower() for word in FORBIDDEN_WORDS):
            raise forms.ValidationError(f"Запрещено использовать запрещённые слова в названии версии.")
        return version_name
