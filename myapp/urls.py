# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_resume, name='upload_resume'),
    path('list/', views.resume_list, name='resume_list'),
]
