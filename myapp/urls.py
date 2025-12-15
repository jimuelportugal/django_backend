# jimuelportugal/django_backend/django_backend-3d58b6cfb12f4c38ac20f9a47212cd341c7d372e/myapp/urls.py

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
    # 1. HOME PAGE: Maps http://127.0.0.1:8000/ to the welcome page
    path('', home_view, name='home'),
    
    # 2. BOOK LIST (The Books Website Section - view books)
    path('books/', BookListView.as_view(), name='books_list'),
    
    # 3. BOOK CRUD (Edit, Delete, Add)
    path('books/add/', BookCreateView.as_view(), name='book_add'),
    path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='book_edit'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    
    # 4. JSON API ENDPOINT (For React/Frontend consumption)
    path('api/', include(router.urls)),
]