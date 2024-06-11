from django.db import models
from help.choices import common as CHOICE
from shift import models as MODEL_SHIF

class Attendance(models.Model):
    employee = models.CharField(max_length=10, choices=CHOICE.EMPLOYEE)
    intime = models.DateTimeField()
    outtime = models.DateTimeField()
    date = models.DateField()
    shift = models.ManyToManyField(MODEL_SHIF.Shift, blank=True)

    def __str__(self):
        return f'{self.employee} - {self.intime} - {[shift.name for shift in self.shift.all()]}'
    class Meta:
        constraints = [models.UniqueConstraint(fields=['employee', 'intime'], name='attendance_employeeintime')]