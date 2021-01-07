from django.db.models import Model


class ColorCombination(Model):

    class Meta:
        db_table = 'app_color_combination'
