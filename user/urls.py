from django.urls import path
from . import views

urlpatterns = [
    path('islogin/',views.isLogin,name='islogin'),
    path('login/', views.login, name='login'),
    path('login_for_medal/', views.login_for_medal, name='login_for_medal'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('userinfo/', views.user_info, name='user_info'),
    path('change_nickname/',views.change_nickname,name='change_nickname'),
    path('bind_email/',views.bind_email,name='bind_email'),
    path('send_email_code/',views.send_verification_code,name='send_verification_code'),
    path('change_password/',views.change_password,name='change_password'),
    path('forget_password/',views.forget_password,name='forget_password'),
]