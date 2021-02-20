from django.db.models import Model


class StaticDesign(Model):

    class Meta:
        db_table = 'app_static_design'
