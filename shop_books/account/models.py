from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    smartphone_number = models.CharField(null=True, blank=True, max_length=64)
    date_of_birth = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.username
