from django.db import models

class Effect(models.Model):

    effect = models.CharField(max_length=50)

    class Meta:
        db_table = 'effect'


class User(models.Model):

    username = models.CharField(max_length=50)
    token = models.UUIDField()
