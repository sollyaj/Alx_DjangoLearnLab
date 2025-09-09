retrieved_book = Book.objects.get(id=book.id)
print(retrieved_book.id, retrieved_book.title, retrieved_book.author, retrieved_book.published_year)
# Expected Output: 1 1984 George Orwell 1949
