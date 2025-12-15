# jimuelportugal/django_backend/django_backend-3d58b6cfb12f4c38ac20f9a47212cd341c7d372e/myapp/views.py

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from django.urls import reverse_lazy # <-- ADDED
from django.views.generic import ListView, CreateView, UpdateView, DeleteView # <-- ADDED

from .models import Book
from .serializers import BookSerializer
from .forms import BookForm 

# --- HTML Views for the Website ---

def home_view(request):
    """Renders the welcome page. Stays namespaced: myapp/templates/myapp/home.html"""
    return render(request, 'home.html')

class BookListView(ListView):
    """Displays the list of books (the 'view books' page)."""
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'
    
class BookCreateView(CreateView):
    """Handles adding a new book."""
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'
    success_url = reverse_lazy('books_list') 

class BookUpdateView(UpdateView):
    """Handles editing an existing book."""
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'
    success_url = reverse_lazy('books_list')

class BookDeleteView(DeleteView):
    """Handles deleting a book."""
    model = Book
    template_name = 'book_confirm_delete.html'
    success_url = reverse_lazy('books_list')

# --- API View (Stays the same for JSON data) ---
class BookViewSet(viewsets.ModelViewSet):
    """Handles standard CRUD operations for Books (JSON API at /api/books/)."""
    queryset = Book.objects.all().order_by('book_id')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]