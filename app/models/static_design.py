from django.db.models import Model, CharField, BooleanField


# TODO: delete all StaticDesign (active = True) on /commands/reset
# TODO: delete all StaticDesign (active = True) after the FIRST user gets logged in (on /token)

class StaticDesign(Model):

    name = CharField(null=True, max_length=256)
    active = BooleanField(null=False, default=False)
    is_on = BooleanField(null=False, default=True)

    class Meta:
        db_table = 'app_static_design'
