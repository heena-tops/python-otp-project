from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('signup',views.signup,name="signup"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('change_pswd',views.change_pswd,name="change_pswd"),
    path('forgot_pswd',views.forgot_pswd,name="forgot_pswd"),
    path('verify_otp',views.verify_otp,name="verify_otp"),
    path('new_pswd',views.new_pswd,name="new_pswd"),
    
]
