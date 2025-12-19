# myapp/forms.py
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'image_link']
        widgets = {
            'title': forms.TextInput(attrs={'style': 'width: 100%; padding: 8px;'}),
            'image_link': forms.URLInput(attrs={'style': 'width: 100%; padding: 8px;'}),
        }