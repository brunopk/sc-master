from django.db.models import Model, CharField, SmallIntegerField

# TODO: associate color to users


class Color(Model):

    hex = CharField(max_length=6)
    red = SmallIntegerField()
    green = SmallIntegerField()
    blue = SmallIntegerField()
