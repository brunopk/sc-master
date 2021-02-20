from django.db.models import Model, CharField, BooleanField


# TODO: active field should set on False for every instance after invoking /commands/reset
# TODO: active field should set on False for every instance after the FIRST user gets logged in (with /token)

class StaticDesign(Model):

    name = CharField(null=True, max_length=256)
    active = BooleanField(null=False, default=False)

    class Meta:
        db_table = 'app_static_design'
