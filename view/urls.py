from django.urls import path
from .views import Overview

app_name = "view"
urlpatterns = [
    path("overview", Overview.as_view(), name="overview"),
]
