from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book

class HomePageView(TemplateView):
    model = Book
    template_name = 'myapp/home.html'

class BookListView(ListView):
    model = Book
    template_name = 'myapp/book_list.html'
    context_object_name = 'books'

class BookDetailView(DetailView):
    model = Book
    template_name = 'myapp/book_detail.html'
    context_object_name = 'book'

class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'author', 'description', 'published_date', 'isbn', 'image']
    template_name = 'myapp/book_form.html'
    success_url = '/books/'

class BookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'author', 'description', 'published_date', 'isbn', 'image']
    template_name = 'myapp/book_form.html'
    success_url = '/books/' 

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'myapp/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')
