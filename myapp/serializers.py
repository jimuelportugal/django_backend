# myapp/serializers.py
from rest_framework import serializers
from .models import User, Position, Book

# --- User Serializers ---
class UserSerializer(serializers.ModelSerializer):
    """For retrieving user data (no password)."""
    class Meta:
        model = User
        fields = ('id', 'username', 'role', 'created_at')
        read_only_fields = ('id', 'role', 'created_at')

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Handles new user creation and password hashing (createUser in users.service.ts)."""
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        # Uses the custom manager's create_user method for hashing
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', 'user')
        )
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    """Handles user updates (updateUser in users.service.ts)."""
    class Meta:
        model = User
        fields = ('username', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True, 'required': False}}
        
    def update(self, instance, validated_data):
        # Handles new password hashing if provided
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
            
        return super().update(instance, validated_data)

# --- Position Serializer ---
class PositionSerializer(serializers.ModelSerializer):
    """Serializes Position model data."""
    # Maps the Foreign Key back to the user's ID for POST/PUT/PATCH
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    # Adds the username of the user who created it, similar to an implicit join.
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Position
        fields = ('id', 'position_code', 'position_name', 'user_id', 'username', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'username')

# --- Book Serializer ---
class BookSerializer(serializers.ModelSerializer):
    """Serializes Book model data."""
    # Includes borrower's username, as done in books.service.ts findById/getAllBooks joins.
    borrower_username = serializers.CharField(source='borrower.username', read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'image_link', 'borrower_id', 'borrower_username', 'status', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'borrower_username')