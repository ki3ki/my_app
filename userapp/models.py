from django.contrib.auth.models import AbstractUser
from django.db import models
from adminapp.models import App
from django.conf import settings

class CustomUser(AbstractUser):
    points = models.PositiveIntegerField(default=0)
    is_admin = models.BooleanField(default=False)


    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE
    )
    points_earned = models.PositiveIntegerField(default=0)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username



class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to='screenshots/')
    completed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')  # Added status field
    description = models.TextField(null=True, blank=True)  # Added description field

    def __str__(self):
        return f"{self.user.username} - {self.app.name}"

