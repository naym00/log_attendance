from django.urls import path
from log import views

urlpatterns = [
    path('get-log/', views.getLog, name='get-log'),
    path('add-log/', views.addLog, name='add-log'),
]