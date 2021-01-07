from django.db.models import Model, CharField, SmallIntegerField


class Color(Model):

    # Hexadecimal value
    id = CharField(primary_key=True, max_length=7)
    red = SmallIntegerField()
    green = SmallIntegerField()
    blue = SmallIntegerField()
