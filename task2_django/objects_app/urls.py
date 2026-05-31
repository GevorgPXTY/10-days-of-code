from django.urls import path
from . import views

urlpatterns = [
    path('', views.objects_list, name='objects_list'),
]
