# jimuelportugal/django_backend/django_backend-948c10cabed393f457a49aefbd8b1711d45732b7/myapp/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from .models import User, Book, Position
from .serializers import (
    UserSerializer, 
    UserRegistrationSerializer, 
    UserUpdateSerializer, 
    PositionSerializer, 
    BookSerializer
)

# NOTE ON PERMISSIONS: For a production application, you would implement custom permissions
# (e.g., IsAdmin, IsOwnerOrAdmin) to strictly enforce the 'role' logic used in the NestJS application.
# For this conversion, we use basic DRF permissions as a placeholder.

# --- Users Views (Mimics users.service.ts) ---

class UserViewSet(viewsets.ModelViewSet):
    """
    Handles standard CRUD operations for Users (users.service.ts)
    Uses different serializers for creation and updates to handle password logic.
    """
    queryset = User.objects.all().order_by('id')
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create': # createUser
            return UserRegistrationSerializer
        if self.action in ['update', 'partial_update']: # updateUser
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create': 
            self.permission_classes = [permissions.AllowAny] # Allow registration
        return [permission() for permission in self.permission_classes]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def find_by_refresh_token(self, request):
        """Mimics users.service.ts -> findByRefreshToken."""
        token = request.data.get('refresh_token')
        if not token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(refresh_token=token)
            return Response(UserSerializer(user).data)
        except User.DoesNotExist:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def set_refresh_token(self, request, pk=None):
        """Mimics users.service.ts -> setRefreshToken."""
        user = self.get_object()
        # In a real setup, this endpoint should only be accessible by the user or an admin
        refresh_token = request.data.get('refresh_token', None)
        user.refresh_token = refresh_token
        user.save(update_fields=['refresh_token'])
        return Response({'status': 'refresh token set'}, status=status.HTTP_200_OK)


# --- Positions Views (Mimics positions.service.ts) ---

class PositionViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Positions (positions.service.ts)
    """
    queryset = Position.objects.select_related('user').all().order_by('id')
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAuthenticated] # Assume admin access is required

    def create(self, request, *args, **kwargs):
        """Mimics positions.service.ts -> createPositions, associating with the logged-in user."""
        try:
            # The FK 'user_id' is expected in the serializer's validated_data, 
            # we inject the authenticated user's ID as the 'user_id'
            data = request.data.copy()
            data['user_id'] = request.user.id
            
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            # Catch UNIQUE constraint violation
            return Response({'error': 'A position with this code or name already exists.'}, status=status.HTTP_400_BAD_REQUEST)


# --- Books Views (Mimics books.service.ts) ---

class BookViewSet(viewsets.ModelViewSet):
    """
    Handles standard CRUD and custom actions for Books (books.service.ts)
    """
    queryset = Book.objects.select_related('borrower').all().order_by('id')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def borrowed(self, request):
        """Mimics books.service.ts -> getBorrowedBooks."""
        user_id = request.user.id
        borrowed_books = self.queryset.filter(
            borrower_id=user_id, 
            status__in=['requested', 'borrowed']
        ) #
        serializer = self.get_serializer(borrowed_books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def request_book(self, request, pk=None):
        """Mimics books.service.ts -> requestBook."""
        user_id = request.user.id
        book = get_object_or_404(Book, pk=pk)

        if book.status != 'available':
            # Matches NestJS BadRequestException
            return Response({'error': 'Book is not available for request.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check for existing request
        if Book.objects.filter(borrower_id=user_id, pk=pk, status='requested').exists():
            return Response({'error': 'You already have an active request for this book.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update book status
        book.borrower_id = user_id
        book.status = 'requested'
        book.save(update_fields=['borrower_id', 'status'])
        
        return Response({'success': True, 'bookId': pk, 'userId': user_id}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def cancel_request(self, request, pk=None):
        """Mimics books.service.ts -> cancelRequest."""
        user_id = request.user.id
        book = get_object_or_404(Book, pk=pk)

        if book.status != 'requested':
            return Response({'error': 'Book is not currently requested or request status is invalid.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if book.borrower_id != user_id:
            return Response({'error': 'You can only cancel your own request.'}, status=status.HTTP_403_FORBIDDEN) # 403 for unauthorized action

        # Update book status
        book.borrower_id = None
        book.status = 'available'
        book.save(update_fields=['borrower_id', 'status'])
        
        return Response({'success': True, 'bookId': pk, 'userId': user_id}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        """Mimics books.service.ts -> returnBook."""
        book = get_object_or_404(Book, pk=pk)

        if book.status != 'borrowed':
            return Response({'error': 'Book is not currently borrowed.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update book status
        book.status = 'available'
        book.borrower_id = None
        book.save(update_fields=['status', 'borrower_id'])
        
        return Response({'success': True, 'message': 'Book returned successfully'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject_request(self, request, pk=None):
        """Mimics books.service.ts -> rejectRequest (requires admin permission)."""
        # Ensure a proper IsAdmin permission check is in place for this action in production
        
        book = get_object_or_404(Book, pk=pk)

        if book.status != 'requested' or book.borrower_id is None:
            return Response({'error': 'No active request found for this book.'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Update book status
        book.borrower_id = None
        book.status = 'available'
        book.save(update_fields=['borrower_id', 'status'])

        return Response({'success': True, 'message': 'Request rejected.'}, status=status.HTTP_200_OK)