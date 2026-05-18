from django.shortcuts import render, get_object_or_404
from .models import Tournament, Team, Match
from django.db.models import F

def index(request):
    turnirs = Tournament.objects.all().order_by('-date')
    context = {
        'turnirs': turnirs
    }
    return render(request, 'Turnir/index.html', context)

def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    
    if tournament.is_finished:
        # Для завершенных турниров сортируем по лиге и занятому месту
        teams = Team.objects.filter(tournament=tournament).order_by('-league__name', 'place')
    else:
        # Для предстоящих турниров сортируем по рейтингу
        teams = Team.objects.filter(tournament=tournament).annotate(
            total_rating=F('player_1__rating') + F('player_2__rating')
        ).order_by('-league__name', '-total_rating')
        
    matches = Match.objects.filter(tournament=tournament).order_by('court', 'id')
    
    context = {
        'tournament': tournament,
        'teams': teams,
        'matches': matches,
    }
    return render(request, 'Turnir/tournament_detail.html', context)