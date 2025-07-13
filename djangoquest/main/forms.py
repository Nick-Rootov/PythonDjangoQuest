from .models import *
from django.forms import ModelForm, TextInput, Textarea


class CitationForm(ModelForm):
    class Meta:
        model = Citation
        fields = ["title", "film"]
        widgets = {
            "title": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите цитату'
            }),
            "film": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фильм'
            }),
        }