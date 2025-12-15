# jimuelportugal/django_backend/django_backend-948c10cabed393f457a49aefbd8b1711d45732b7/myapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

# --- Custom User Manager ---
class CustomUserManager(BaseUserManager):
    """Custom user model manager, handles user and superuser creation."""
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password) # Handles password hashing, like bcrypt in NestJS service
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

# --- 1. User Model ---
class User(AbstractBaseUser, PermissionsMixin):
    """Mirrors the 'users' table in scheme.sql."""
    username = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=50, default='user')
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Required fields for Django's user system
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'users'

# --- 2. Position Model ---
class Position(models.Model):
    """Mirrors the 'positions' table in scheme.sql."""
    position_code = models.CharField(max_length=100, unique=True)
    position_name = models.CharField(max_length=300, unique=True)
    # Foreign key to User, matching the 'id' column from scheme.sql
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'positions'
        
    def __str__(self):
        return self.position_name

# --- 3. Book Model ---
class Book(models.Model):
    """Mirrors the 'books' table in scheme.sql."""
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('requested', 'Requested'),
        ('borrowed', 'Borrowed'),
    )
    
    title = models.CharField(max_length=255, unique=True)
    image_link = models.CharField(max_length=512, null=True, blank=True)
    # Foreign key to User, can be NULL, matching 'borrower_id'
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='borrower_id')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'books'
        
    def __str__(self):
        return self.title