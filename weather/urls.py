from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('forecast/', views.forecast, name='forecast'),
    path('alerts/', views.alerts, name='alerts'),
    path('schedule/', views.schedule_task, name='schedule_task'),
]
