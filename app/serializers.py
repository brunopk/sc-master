from rest_framework import serializers
from app import models

class Effect(serializers.ModelSerializer):

    class Meta:
        model = models.Effect
        fields = '__all__'


