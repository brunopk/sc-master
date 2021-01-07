from django.db.models import Model, SmallIntegerField, ForeignKey, CASCADE, UUIDField
from app.models.color import Color
from app.models.color_combination import ColorCombination


class Section(Model):

    id = UUIDField(primary_key=True)
    start = SmallIntegerField(null=False)
    end = SmallIntegerField(null=False)
    color = ForeignKey(Color, null=False, on_delete=CASCADE)
    color_combination = ForeignKey(ColorCombination, null=True, on_delete=CASCADE)
