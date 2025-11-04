from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("graficas/", include('graficas.urls')),
    path('admin/', admin.site.urls),

]
