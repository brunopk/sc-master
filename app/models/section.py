from django.db.models import Model, SmallIntegerField, ForeignKey, CASCADE, UUIDField
from app.models import Color, ColorCombination


class Section(Model):

    id = UUIDField(primary_key=True)
    start = SmallIntegerField(null=False)
    end = SmallIntegerField(null=False)
    color = ForeignKey(Color, null=False, on_delete=CASCADE, name='color_hex')
    color_combination = ForeignKey(ColorCombination, null=True, on_delete=CASCADE)
