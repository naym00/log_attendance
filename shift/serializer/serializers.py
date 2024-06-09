from rest_framework import serializers
from shift import models

class Shiftserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shift
        fields='__all__'
        