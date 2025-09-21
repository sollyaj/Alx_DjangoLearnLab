from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdminUser()]
        return super().get_permissions()
    
    # BookList: Read-only list of books, requires authentication
# BookViewSet: Full CRUD with authentication
# - All users can read/create/update
# - Only admins can delete
