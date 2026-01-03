from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('otp/', views.otp_verify, name='otp'),
    path('otp/verify', views.verify_and_enable, name='veerify_and_enable'),
    path('login/', views.login_view, name='login'),
    path('logout', views.logout, name='logout')
] 