from rest_framework import serializers
from attendance import models

class Attendanceserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attendance
        fields='__all__'
        