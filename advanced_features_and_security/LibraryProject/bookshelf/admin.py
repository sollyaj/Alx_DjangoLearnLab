from django.contrib import admin
from .models import Author, Book, Library, Librarian


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_year")
    list_filter = ("published_year", "author")
    search_fields = ("title", "author__name")


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("books",)


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ("name", "library")


