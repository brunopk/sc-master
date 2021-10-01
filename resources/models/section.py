from django.db.models import Model, SmallIntegerField, ForeignKey, CASCADE, CharField
from resources.models import StaticDesign


class Section(Model):

    start = SmallIntegerField(null=False)

    end = SmallIntegerField(null=False)

    color = CharField(null=False, max_length=7)

    static_design = ForeignKey(StaticDesign, null=True, on_delete=CASCADE)
