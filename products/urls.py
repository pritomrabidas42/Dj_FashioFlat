from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail_view, name='product_detail'),
    path('products/<int:pk>/buy/', purchase_product, name='purchase_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)