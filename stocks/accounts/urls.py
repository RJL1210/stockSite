from django.contrib import admin
from django.urls import path, include
from . import views as account_views
from graphs import views

urlpatterns = [
    path('', include('graphs.urls')), #home
    path('login.html/', account_views.login_request, name='login'),
    path('logout/', account_views.logout_request, name='logout'),
    path('register.html/', account_views.register, name='register'),
]