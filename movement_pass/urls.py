from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/login/', views.userlogin, name='login'),
    path('account/logout/', views.userlogout, name='logout'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('apply_pass/', views.ApplyPassView.as_view(), name='apply_pass'),
]