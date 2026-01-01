from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('otp/', views.otp_verify, name='otp'),
] 