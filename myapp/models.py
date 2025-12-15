# jimuelportugal/django_backend/django_backend-948c10cabed393f457a49aefbd8b1711d45732b7/myapp/models.py

from django.db import models
from django.utils import timezone

# --- Book Model (Simplified) ---
class Book(models.Model):
    """Mirrors the simplified 'books' table (no borrower/user dependency)."""
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('requested', 'Requested'),
        ('borrowed', 'Borrowed'),
    )
    
    # Explicitly define the Primary Key
    book_id = models.AutoField(primary_key=True)
    
    title = models.CharField(max_length=255, unique=True)
    image_link = models.CharField(max_length=512, null=True, blank=True)
    
    # borrower_id foreign key and dependency on 'users' table are removed.
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'books'
        
    def __str__(self):
        return self.title