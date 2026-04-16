from django.contrib import admin
from .models import League, Tournament, Team

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'points_1', 'points_2', 'points_3', 'points_4', 'points_other')

class TeamInline(admin.TabularInline):
    model = Team
    extra = 1
    fields = ('player_1', 'player_2', 'league', 'place')

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
    inlines = [TeamInline]