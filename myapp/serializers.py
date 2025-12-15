# jimuelportugal/django_backend/django_backend-948c10cabed393f457a49aefbd8b1711d45732b7/myapp/serializers.py

from rest_framework import serializers
from .models import Book

# --- Book Serializer (Simplified) ---
class BookSerializer(serializers.ModelSerializer):
    """Serializes simplified Book model data."""
    
    class Meta:
        model = Book
        # Fields correspond directly to the simplified Book model
        fields = ('book_id', 'title', 'image_link', 'status', 'created_at', 'updated_at')
        read_only_fields = ('book_id', 'created_at', 'updated_at')