from django.contrib import admin
from django.urls import path, include
from .  import views


urlpatterns = [
    path('',views.index,name="index"),
    path('login',views.logIn,name="login"),
    path('signup',views.signUp,name="signup"),
    path('home',views.home,name="home"),
    path('sendcoin',views.sendCoin,name="sendcoin"),
    path('api_crypto',views.api_view,name="api_view"),
    path('logout',views.logout,name="logout"),

]

