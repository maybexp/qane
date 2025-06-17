from django.urls import path
from . import views

urlpatterns = [
    path('privacy-policy', views.privacyPolicy, name="privacyPolicy"),
    path('about', views.about, name="about"),
]
