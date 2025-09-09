from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from django.views.generic import DetailView
from .models import Library


# Function-based view to list all books
def book_list(request):
    books = Book.objects.all()
    output = "<h2>Book List</h2><ul>"
    for book in books:
        output += f"<li>{book.title} (by {book.author})</li>"
    output += "</ul>"
    return HttpResponse(output)

class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"



