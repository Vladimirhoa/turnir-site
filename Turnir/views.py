from django.shortcuts import render
from .models import Tournament, Team

def index(request):
    turnirs = Tournament.objects.all()
    context = {
        'turnirs': turnirs
    }
    return render(request, 'Turnir/index.html', context)

def tournament_detail(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    teams = Team.objects.filter(tournament=tournament).order_by('-league__name', 'place')
    context = {
        'tournament': tournament,
        'teams': teams
    }
    return render(request, 'Turnir/tournament_detail.html', context)