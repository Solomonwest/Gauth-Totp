from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('otp/', views.otp_verify, name='otp'),
    path('login/', views.login_view, name='login'),
] 