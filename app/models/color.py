from django.db.models import Model, CharField, SmallIntegerField


class Color(Model):

    # Hexadecimal value
    hex = CharField(primary_key=True, max_length=6)
    red = SmallIntegerField()
    green = SmallIntegerField()
    blue = SmallIntegerField()
