from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# their two type of clas user and customuser ...by cutomeruser we can add more fields in form 
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('investor', 'Investor'),
        ('entrepreneur', 'Entrepreneur'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    available_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    first_login = models.BooleanField(default=True)

    def __str__(self):
        return self.username