from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book


@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    """List all books (requires can_view permission)."""
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


@permission_required("bookshelf.can_create", raise_exception=True)
def create_book(request):
    return HttpResponse("Book creation form here (protected by can_create).")


@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"Editing {book.title} (protected by can_edit).")


@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"Deleting {book.title} (protected by can_delete).")


