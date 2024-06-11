from django.urls import path, register_converter
from attendance.converters import DateConverter
from attendance import views
register_converter(DateConverter, 'date')

urlpatterns = [
    path('get-attendance/', views.getAttendance, name='get-attendance'),
    path('generate-attendance/<date:fromdate>/<date:todate>', views.generateAttendance, name='generate-attendance'),
]
