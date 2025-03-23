from django.urls import path
from . import views

urlpatterns = [
    path('dish_list/', views.dish_list, name='dish_list'),
    path('vote/', views.vote_dish, name='vote_dish'),
    path('add_dish/', views.add_dish, name='add_dish'),
    path('winning_dish/', views.winning_dish, name='winning_dish'),
    # ... alte URL-uri
]