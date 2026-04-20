from django.shortcuts import render
from .models import Athlete
from Turnir.models import Team, Match
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
    finished_matches = Match.objects.filter(
        (Q(team1__in=teams) | Q(team2__in=teams)),
        is_finished=True
    )
    total_matches = finished_matches.count()
    wins = 0
    for match in finished_matches:
        if match.who_win in teams:
            wins += 1
    win_percentage = round((wins / total_matches) * 100) if total_matches > 0 else 0
    context = {
        'athlete': athlete,
        'teams': teams,
        'win_percentage': win_percentage,
        'total_matches': total_matches,
        'wins': wins
    }
    return render(request, 'Athlete/athlete_detail.html', context)