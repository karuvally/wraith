from django.urls import path, include

app_name = "login"
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
]
