# jimuelportugal/django_backend/django_backend-948c10cabed393f457a49aefbd8b1711d45732b7/myapp/views.py

from rest_framework import viewsets
from rest_framework.permissions import AllowAny # Explicitly allow unauthenticated access
from .models import Book
from .serializers import BookSerializer

# --- Books Views (Public CRUD) ---

class BookViewSet(viewsets.ModelViewSet):
    """
    Handles standard CRUD operations for Books (Create, Retrieve, Update, Delete).
    This API is now publicly accessible (unauthenticated).
    """
    queryset = Book.objects.all().order_by('book_id')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    # All user-dependent custom actions (request_book, cancel_request, etc.) are removed.