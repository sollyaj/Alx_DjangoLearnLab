# CRUD Operations for Book Model

## Create
```python
book = Book.objects.create(title="1984", author="George Orwell", published_year=1949)
print(book)
# Expected Output: 1984

retrieved_book = Book.objects.get(id=book.id)
print(retrieved_book.id, retrieved_book.title, retrieved_book.author, retrieved_book.published_year)
# Expected Output: 1 1984 George Orwell 1949

retrieved_book.title = "Nineteen Eighty-Four"
retrieved_book.save()
print(retrieved_book.title)
# Expected Output: Nineteen Eighty-Four

retrieved_book.delete()
print(Book.objects.all())
# Expected Output: <QuerySet []>

