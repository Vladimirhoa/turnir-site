from django.shortcuts import render, get_object_or_404
from .models import Tournament, Team, Match

def index(request):
    turnirs = Tournament.objects.all()
    context = {
        'turnirs': turnirs
    }
    return render(request, 'Turnir/index.html', context)

def tournament_detail(request, tournament_id):
    # Используем get_object_or_404 для безопасности
    tournament = get_object_or_404(Tournament, id=tournament_id)
    
    # Список команд для вкладки "Участники/Результаты"
    teams = Team.objects.filter(tournament=tournament).order_by('-league__name', 'place')
    
    matches = Match.objects.filter(tournament=tournament).order_by('court', 'id')
    
    context = {
        'tournament': tournament,
        'teams': teams,
        'matches': matches,
    }
    return render(request, 'Turnir/tournament_detail.html', context)