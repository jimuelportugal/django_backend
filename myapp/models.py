from django.db import models

class Book(models.Module):
    title = models.charField(max_lenght=100)
    author = models.charField(max_lenght=100)
    
    def __str__(self):
        return self.title
