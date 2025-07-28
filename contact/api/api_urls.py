# contact/api_urls.py

from django.urls import path
from .api_views import ContactFormAPIView

urlpatterns = [
    path('contact/', ContactFormAPIView.as_view(), name='api-contact'),
]
