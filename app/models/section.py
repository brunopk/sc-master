from django.db.models import Model, SmallIntegerField, ForeignKey, CASCADE, UUIDField, CharField
from app.models import Color, StaticDesign


# TODO: add field 'is_on' boolean
# TODO: change 'name='color_hex'

class Section(Model):

    start = SmallIntegerField(null=False)
    end = SmallIntegerField(null=False)
    color = ForeignKey(Color, null=False, on_delete=CASCADE, name='color_hex')
    sc_rpi_id = UUIDField(null=True)
    name = CharField(null=True, max_length=256)
    static_design = ForeignKey(StaticDesign, null=True, on_delete=CASCADE)
