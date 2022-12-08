from secrets import choice
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    choices_cargo = (('V', 'Vendedor'),
                     ('G', 'Gerente'))
    cargo = models.CharField(max_length = 1, choices=choices_cargo)
    
    
    
