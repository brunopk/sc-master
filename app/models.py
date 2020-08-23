from django.db import models
from django.contrib.auth.models import AbstractUser

class Effect(models.Model):

    effect = models.CharField(max_length=50)

# Attributes added to this model will be added to django.contrib.auth.models.AbstractUser (default user model in Django)
class User(AbstractUser):
    pass