from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', views.upload_resume, name='upload_resume'),
    path('resumes/', views.resume_list, name='resume_list'),
]
