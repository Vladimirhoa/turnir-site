from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:tournament_id>/', views.tournament_detail, name='tournament_detail')
]