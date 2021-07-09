from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.userlogin, name='login'),
    path('accounts/logout/', views.userlogout, name='logout'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('apply_pass/', views.ApplyPassView.as_view(), name='apply_pass'),
    path('apply_pass_list/', views.ApplyPassList.as_view(), name='apply_pass_list'),
    path('apply_pass_download_page/', views.apply_pass_download_page, name='apply_pass_download_page'),
]