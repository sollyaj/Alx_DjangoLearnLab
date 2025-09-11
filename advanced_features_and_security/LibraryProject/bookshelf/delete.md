
from bookshelf.models import Book

# DELETE
retrieved_book.delete()
print(Book.objects.all())
# Expected Output: <QuerySet []> confirming the deletion

