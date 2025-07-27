from django.urls import path
from .api_views import PaymentListCreateAPIView

urlpatterns = [
    path('payments/', PaymentListCreateAPIView.as_view(), name='payment-list-create'),
]
