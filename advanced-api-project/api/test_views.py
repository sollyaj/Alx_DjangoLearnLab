from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()

        # Create an author and a book
        self.author = Author.objects.create(name="George Orwell")
        self.book = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author
        )

        # Endpoints
        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", kwargs={"pk": self.book.pk})
        self.create_url = reverse("book-create")
        self.update_url = reverse("book-update", kwargs={"pk": self.book.pk})
        self.delete_url = reverse("book-delete", kwargs={"pk": self.book.pk})

    # ---------- CRUD TESTS ----------

    def test_list_books(self):
        """Ensure the list endpoint returns all books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "1984")

    def test_retrieve_book_detail(self):
        """Ensure detail endpoint returns a single book"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "1984")

    def test_create_book_requires_authentication(self):
        """Ensure unauthenticated users cannot create"""
        response = self.client.post(self.create_url, {
            "title": "Animal Farm",
            "publication_year": 1945,
            "author": self.author.id,
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated(self):
        """Ensure authenticated users can create a book"""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(self.create_url, {
            "title": "Animal Farm",
            "publication_year": 1945,
            "author": self.author.id,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book_authenticated(self):
        """Ensure authenticated users can update a book"""
        self.client.login(username="testuser", password="password123")
        response = self.client.put(self.update_url, {
            "title": "Nineteen Eighty-Four",
            "publication_year": 1949,
            "author": self.author.id,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Nineteen Eighty-Four")

    def test_delete_book_authenticated(self):
        """Ensure authenticated users can delete a book"""
        self.client.login(username="testuser", password="password123")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    # ---------- FILTERING / SEARCH / ORDERING ----------

    def test_filter_books_by_title(self):
        response = self.client.get(self.list_url, {"title": "1984"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "1984")

    def test_search_books_by_author_name(self):
        response = self.client.get(self.list_url, {"search": "Orwell"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "1984")

    def test_order_books_by_publication_year(self):
        # Create a second book with a different year
        Book.objects.create(title="Animal Farm", publication_year=1945, author=self.author)
        response = self.client.get(self.list_url, {"ordering": "publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years))
