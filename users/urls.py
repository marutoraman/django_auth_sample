from django.urls import path, include
from .views import logout_auth0

app_name = "users"
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
    path('logout', logout_auth0, name="logout"),
]