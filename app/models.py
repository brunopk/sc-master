from django.db.models import Model, CASCADE, CharField, SmallIntegerField, ForeignKey
from django.contrib.auth.models import AbstractUser
from app.scp import ApiClient

scp = ApiClient()
scp.connect()
scp_ok = 200


# Attributes added to this model will be added to django.contrib.auth.models.AbstractUser (default user model in Django)
class User(AbstractUser):
    pass


class Color(Model):

    hex = CharField(max_length=7)
    red = SmallIntegerField()
    green = SmallIntegerField()
    blue = SmallIntegerField()
