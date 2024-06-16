# resume_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', include('myapp.urls')),
    path('resumes/', include('myapp.urls')),
]
