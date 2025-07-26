# products/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', product_list, name='product-list'),
    path('product/<int:pk>/', product_detail, name='product-detail'),
    path('product/<int:product_id>/review/', submit_review, name='submit-review'),
]
