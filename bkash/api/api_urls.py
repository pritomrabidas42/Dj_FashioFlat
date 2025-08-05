from django.urls import path
from .api_views import bkash_initiate_payment, bkash_execute_payment, get_bkash_payment_details

urlpatterns = [
    path('initiate/', bkash_initiate_payment, name='bkash_initiate_payment'),
    path('execute/', bkash_execute_payment, name='bkash_execute_payment'),
    path('details/<int:order_id>/', get_bkash_payment_details, name='bkash_payment_details'),
]
