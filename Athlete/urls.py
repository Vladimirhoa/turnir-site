from django.urls import path
from . import views

urlpatterns = [
    path('', views.leaderboard, name='leaderboard'),
    path('<int:athlete_id>/', views.Athlete_detail, name='athlete_detail')
]