from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model for the application.
    Extends Django's AbstractUser to add custom fields.
    """
    # Other custom fields can be added here
    birth_date = models.DateField(null=True, blank=True)
    about_me = models.TextField(blank=True)
    picture_profile = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)


    # Add related_name to groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='custom_user_set',  # Change this name
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',  # Change this name
        related_query_name='user',
    )

    def __str__(self):
        return self.username  # Or return self.email

# Example of another model (if needed)
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # ... other profile fields