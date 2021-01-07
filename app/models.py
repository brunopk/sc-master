from django.db.models import Model, CharField, SmallIntegerField, ForeignKey, CASCADE, UUIDField
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


class ColorCombination(Model):

    class Meta:
        db_table = 'app_color_combination'


class Section(Model):

    id = UUIDField(primary_key=True)
    start = SmallIntegerField(null=False)
    end = SmallIntegerField(null=False)
    color = ForeignKey(Color, null=False, on_delete=CASCADE)
    color_combination = ForeignKey(ColorCombination, null=True, on_delete=CASCADE)
