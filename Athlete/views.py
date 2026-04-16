from django.shortcuts import render
from .models import Athlete
from Turnir.models import Team
from django.db.models import Q

def leaderboard(request):
    male_athletes = Athlete.objects.filter(gender='M').order_by('-rating')
    female_athletes = Athlete.objects.filter(gender='F').order_by('-rating')
    
    context = {
        'male_athletes': male_athletes,
        'female_athletes': female_athletes
    }
    return render(request, 'Athlete/leaderboard.html', context)

def Athlete_detail(request, athlete_id):
    athlete = Athlete.objects.get(id=athlete_id)
    teams = Team.objects.filter(Q(player_1 = athlete) | Q(player_2 = athlete)).order_by('-tournament__date')
    context = {
        'athlete': athlete,
        'teams': teams
    }
    return render(request, 'Athlete/athlete_detail.html', context)