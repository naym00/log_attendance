from django.urls import path
from log import views

urlpatterns = [
    path('get-log/', views.getLog, name='get-log'),
    path('add-log/', views.addLog, name='add-log'),
    path('update-log/<int:logid>/', views.updateLog, name='update-log'),
]