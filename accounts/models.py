from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', default='default.jpg')
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=4, blank=True, null=True)

    def _str__(self):
        return self.username


