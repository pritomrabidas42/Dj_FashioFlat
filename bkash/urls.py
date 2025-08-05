from django.urls import path
from .views import *

urlpatterns = [
    path('<int:order_id>/', bkash_payment, name='bkash_payment'),
    path('callback/<int:order_id>/', bkash_callback, name='bkash_callback'),
    path('success/', payment_success_page, name='payment_success_page'),
    path('cancel/', payment_cancel_page, name='payment_cancel_page'),
]
