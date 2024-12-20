from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myinfo/', include('myinfo_app.urls')),  # Adjust the path if the app name differs
]
