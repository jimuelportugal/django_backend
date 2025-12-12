from django.urls import path
from .views import BookListView, HomePageView, BookCreateView, BookUpdateView, BookDeleteView, BookListView, BookDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('books/', BookListView.as_view(), name="book_list"),
    path('book/<int:pk>/', BookDetailView.as_view(), name="book_detail"),
    path('book/new/', BookCreateView.as_view(), name="book_create"),
    path('book/<int:pk>/edit/', BookUpdateView.as_view(), name="book_update"),
    path('book/<int:pk>/delete', BookDeleteView.as_view(), name="book_delete"),
]