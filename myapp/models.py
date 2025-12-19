from django.db import models
from django.utils import timezone

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    image_link = models.CharField(max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'books'
        
    def __str__(self):
        return self.title