from django.urls import path
from .api_views import CartItemListCreateAPIView, CartItemDetailAPIView

urlpatterns = [
    path('cart/', CartItemListCreateAPIView.as_view(), name='cart-list-create'),
    path('cart/<int:pk>/', CartItemDetailAPIView.as_view(), name='cart-detail'),
]
