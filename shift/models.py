from django.db import models

class Shift(models.Model):
    name = models.CharField(max_length=10, unique=True)
    start_at = models.TimeField()
    end_at = models.TimeField()

    def __str__(self):
        return f'{self.name} - {self.start_at} - {self.end_at}'
    class Meta:
        constraints = [models.UniqueConstraint(fields=['name', 'start_at'], name='namestart_at')]