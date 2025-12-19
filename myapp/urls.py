from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet, 
    home_view, 
    BookListView, 
    BookCreateView, 
    BookUpdateView, 
    BookDeleteView
)

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', home_view, name='home'),
    path('books/', BookListView.as_view(), name='books_list'),
    path('books/add/', BookCreateView.as_view(), name='book_add'),
    path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='book_edit'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('api/', include(router.urls)),
]