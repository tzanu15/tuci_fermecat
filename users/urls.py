from django.urls import path
from . import views  # Sau unde se află view-urile tale
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.user_profile, name='profile'),
    # Alte URL-uri ale aplicației
]