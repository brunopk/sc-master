from django.contrib.auth.models import AbstractUser


# Attributes added to this model will be added to django.contrib.auth.models.AbstractUser (default user model in Django)
class User(AbstractUser):
    pass
