from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('2FA_setup/', views.totp_setup, name='totp_setup'),
    path('2FA_verify/', views.totp_setup, name='totp_verify'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout', views.logout, name='logout')
] 