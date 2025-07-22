from django.urls import path
from .views import *
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'), 
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('logout/', logout_view, name='logout'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('forgot_otp/', forgot_otp, name='forgot_otp'),
    path('reset_password/', reset_password, name='reset_password'),
]
