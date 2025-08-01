"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
     path('', include('products.urls')),   
    path('cart/', include('cart.urls')),       
    path('order/', include('orders.urls')),
    path('payment/', include('payments.urls')),
    path('contact/', include('contact.urls')),
    path('api/contact/', include('contact.api.api_urls')),
    path('api/products/', include('products.api.api_urls')),
    path('api/accounts/', include('accounts.api.api_urls')),
    path('api/cart/', include('cart.api.api_urls')),
    path('api/orders/', include('orders.api.api_urls')),
    path('api/payments/', include('payments.api.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)