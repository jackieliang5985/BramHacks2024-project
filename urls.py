# urls.py in the root directory (same as manage.py)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.urls')),  # This will route everything in `backend/urls.py` under `/api/`
]