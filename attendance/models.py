from django.db import models
from help.choices import common as CHOICE
from shift import models as MODEL_SHIF

class Attendance(models.Model):
    employee = models.CharField(max_length=10, choices=CHOICE.EMPLOYEE)
    intime = models.DateTimeField()
    outtime = models.DateTimeField()
    shift = models.ForeignKey(MODEL_SHIF.Shift, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.employee} - {self.intime} - {self.shift.name}'
    class Meta:
        constraints = [models.UniqueConstraint(fields=['employee', 'intime', 'shift'], name='employeeintimeshift')]