from rest_framework import serializers
from log import models

class Logserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Log
        fields='__all__'
        