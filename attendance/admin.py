from django.contrib import admin
from attendance import models

admin.site.register([
    models.Attendance    
])