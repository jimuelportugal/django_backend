# jimuelportugal/django_backend/django_backend-3d58b6cfb12f4c38ac20f9a47212cd341c7d372e/myapp/views.py

# ... (Existing imports)
from .models import Book
from .serializers import BookSerializer
from .forms import BookForm 

# --- HTML Views for the Website ---

def home_view(request):
    """Renders the welcome page. Stays namespaced: myapp/templates/myapp/home.html"""
    return render(request, 'myapp/home.html')

class BookListView(ListView):
    """Displays the list of books (the 'view books' page)."""
    model = Book
    template_name = 'book_list.html' # <--- CHANGED to root path
    context_object_name = 'books'
    
class BookCreateView(CreateView):
    """Handles adding a new book."""
    model = Book
    form_class = BookForm
    template_name = 'book_form.html' # <--- CHANGED to root path
    success_url = reverse_lazy('books_list') 

class BookUpdateView(UpdateView):
    """Handles editing an existing book."""
    model = Book
    form_class = BookForm
    template_name = 'book_form.html' # <--- CHANGED to root path
    success_url = reverse_lazy('books_list')

class BookDeleteView(DeleteView):
    """Handles deleting a book."""
    model = Book
    template_name = 'book_confirm_delete.html' # <--- CHANGED to root path
    success_url = reverse_lazy('books_list')

# ... (Rest of BookViewSet)