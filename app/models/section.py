from django.db.models import Model, SmallIntegerField, ForeignKey, CASCADE, UUIDField
from app.models import Color, StaticDesign


class Section(Model):

    start = SmallIntegerField(null=False)
    end = SmallIntegerField(null=False)
    color = ForeignKey(Color, null=False, on_delete=CASCADE, name='color_hex')
    static_design = ForeignKey(StaticDesign, null=True, on_delete=CASCADE)
