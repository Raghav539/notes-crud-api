from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom manager for handling user creation
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        # Ensure email is provided
        if not email:
            raise ValueError("The Email field must be set")
        # Normalize email (convert to lowercase and clean)
        email = self.normalize_email(email)
        # Create user instance with email and extra fields
        user = self.model(email=email, **extra_fields)
        # Hash and set the password
        user.set_password(password)
        # Save user to the database
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with elevated permissions.
        """
        # Set default superuser permissions
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault('is_active', True)
        
        # Ensure superuser has required permissions
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        # Create superuser using create_user method
        return self.create_user(email, password, **extra_fields)

# Custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Email field used as the unique identifier for authentication
    email = models.EmailField(unique=True)
    # First name of the user, optional
    first_name = models.CharField(max_length=100, blank=True)
    # Last name of the user, optional
    last_name = models.CharField(max_length=100, blank=True)
    # Flag to indicate if account is active
    is_active = models.BooleanField(default=True)
    # Flag to indicate if user can access admin interface
    is_staff = models.BooleanField(default=False)
    
    # Assign the custom manager
    objects = CustomUserManager()  # Corrected from CustomUserManage
    
    # Specify email as the field for authentication
    USERNAME_FIELD = "email"
    # No additional required fields for createsuperuser
    REQUIRED_FIELDS = []
    
    # String representation of the user
    def __str__(self):
        return self.email