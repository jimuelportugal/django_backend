from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Book
from .serializers import BookSerializer
from .forms import BookForm 

def home_view(request):
    return render(request, 'home.html')

class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(title__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BookForm()
        context['search_query'] = self.request.GET.get('q', '')
        return context
    
class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book_form.html' 
    success_url = reverse_lazy('books_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        if context.get('form') and context['form'].errors:
            context['show_modal'] = True
        return context

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'
    success_url = reverse_lazy('books_list')

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book_confirm_delete.html'
    success_url = reverse_lazy('books_list')

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('book_id')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]