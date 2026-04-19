from django.contrib import admin
import re
from .models import League, Tournament, Team, Match 

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'points_1', 'points_2', 'points_3', 'points_4', 'points_other')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    # Разрешаем поиск по фамилиям обоих игроков в команде
    search_fields = ('player_1__last_name', 'player_2__last_name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        referer = request.META.get('HTTP_REFERER', '')
        
        match_url = re.search(r'/tournament/(\d+)/change/', referer)
        
        if match_url:
            tournament_id = match_url.group(1)
            qs = qs.filter(tournament_id=tournament_id)
            
        return qs
    def get_model_perms(self, request):
        return {}


class TeamInline(admin.TabularInline):
    model = Team
    extra = 1
    fields = ('player_1', 'player_2', 'league', 'place')
    autocomplete_fields = ['player_1', 'player_2']

class MatchInline(admin.TabularInline):
    model = Match
    extra = 1
    fields = ('court', 'stage', 'team1', 'team2', 'referee', 'team1_score', 'team2_score', 'is_finished')
    autocomplete_fields = ['team1', 'team2', 'referee']

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'start_time', 'allowed_gender', 'get_age_category_display', 'is_finished')
    list_filter = ('is_finished', 'date', 'allowed_gender')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'date', 'start_time', 'end_time', 'address')
        }),
        ('Возрастные ограничения', {
            'fields': ('birth_year_from', 'birth_year_to'),
            'description': 'Укажите диапазон годов рождения участников'
        }),
        ('Прочее', {
            'fields': ('allowed_gender', 'is_finished')
        }),
    )
    inlines = [TeamInline, MatchInline] 


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'court', 'stage', 'team1', 'team2', 'team1_score', 'team2_score', 'is_finished')
    list_filter = ('tournament', 'court', 'is_finished', 'stage')
    list_editable = ('team1_score', 'team2_score', 'is_finished')
    search_fields = ('team1__player_1__last_name', 'team2__player_1__last_name')