from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    isbn = models.CharField(max_length=13, blank=True, null=True)
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)
    
    def __str__(self):
        return self.title
