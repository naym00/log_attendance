from django.db import models
from help.choices import common as CHOICE

class Log(models.Model):
    employee = models.CharField(max_length=10, choices=CHOICE.EMPLOYEE)
    intime = models.DateField()
    mintime = models.DateField()

    def __str__(self):
        return f'{self.employee} - {self.intime} - {self.mintime}'
    class Meta:
        constraints = [models.UniqueConstraint(fields=['employee', 'intime'], name='employeeintime')]