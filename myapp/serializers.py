from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """Serializes simplified Book model data."""
    
    class Meta:
        model = Book
        fields = ('book_id', 'title', 'image_link','created_at', 'updated_at')
        read_only_fields = ('book_id', 'created_at', 'updated_at')