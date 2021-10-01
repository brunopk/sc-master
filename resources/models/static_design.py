from django.db.models import Model, CharField


class StaticDesign(Model):

    name = CharField(null=True, max_length=256)
