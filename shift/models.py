from django.db import models
from datetime import timedelta
from help.common.generic import Generichelps as ghelp

class Shift(models.Model):
    name = models.CharField(max_length=10, unique=True)
    start_at = models.TimeField()
    end_at = models.TimeField()

    mstart_at = models.TimeField(blank=True, null=True)
    mend_at = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.start_at} - {self.end_at}'
    class Meta:
        constraints = [models.UniqueConstraint(fields=['name', 'start_at'], name='namestart_at')]

    def save(self, *args, **kwargs):
        date_time = ghelp().convert_STR_y_m_d_h_m_s_Dateformat(f'2024-05-05 {self.start_at}') - timedelta(hours=6)
        self.mstart_at = date_time.time()
        date_time = ghelp().convert_STR_y_m_d_h_m_s_Dateformat(f'2024-05-05 {self.end_at}') - timedelta(hours=6)
        self.mend_at = date_time.time()
        super().save(*args, **kwargs)