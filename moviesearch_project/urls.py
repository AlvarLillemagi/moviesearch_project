from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('moviesearch.urls')),
    path('accounts/', include('accounts.urls')),
    path('userprofiles/', include('userprofiles.urls')),
]