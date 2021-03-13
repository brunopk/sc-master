from django.db.models import Model, SmallIntegerField, ForeignKey, CASCADE, UUIDField, CharField, BooleanField
from app.models import Color, StaticDesign


class Section(Model):

    start = SmallIntegerField(null=False)
    end = SmallIntegerField(null=False)
    hw_id = UUIDField(null=True)
    name = CharField(null=True, max_length=256)
    is_on = BooleanField(null=False, default=True)
    color = ForeignKey(Color, null=False, on_delete=CASCADE, related_name='color')
    static_design = ForeignKey(StaticDesign, null=True, on_delete=CASCADE)
