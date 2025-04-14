from django.urls import path
from .views import login, signUp
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('login', LoginView.as_view(), name='login'),
    path('login', login, name='login'),
    path('signUp', signUp, name='signUp'),
    path('', views.register, name='register'),  # Registration is the landing page
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    
]
