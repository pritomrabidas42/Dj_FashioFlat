from django.urls import path
from .views import *

urlpatterns = [
    path('init/<int:order_id>/', initiate_payment, name='initiate_payment'),
    path('success/', payment_success, name='payment_success'),
    path('fail/', payment_fail, name='payment_fail'),
    path('cancel/', payment_cancel, name='payment_cancel'),
]
