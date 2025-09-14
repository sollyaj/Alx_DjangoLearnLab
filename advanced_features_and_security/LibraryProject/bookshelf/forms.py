from django import forms
from .models import Book

# ✅ Secure form for Book model
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "published_year"]

        # Extra security: widget attributes to sanitize inputs
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Book Title"}),
            "author": forms.TextInput(attrs={"placeholder": "Author Name"}),
            "published_year": forms.NumberInput(attrs={"min": 0}),
        }
