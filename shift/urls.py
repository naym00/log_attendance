from django.urls import path
from shift import views

urlpatterns = [
    path('get-shift/', views.getShift, name='get-shift'),
    path('add-shift/', views.addShift, name='add-shift')
]
