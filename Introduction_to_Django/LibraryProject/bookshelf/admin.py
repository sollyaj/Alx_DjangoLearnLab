from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    # Columns to show in the list view
    list_display = ('title', 'author', 'published_year')

    # Add filters on the right-hand side
    list_filter = ('author', 'published_year')

    # Add a search box (can search by title or author)
    search_fields = ('title', 'author')

# Register the Book model with these custom settings
admin.site.register(Book, BookAdmin)

