from django.contrib import admin
from .models import Athlete

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'gender', 'birth_date', 'rating')
    
    search_fields = ('last_name', 'first_name')
    
    list_filter = ('gender',)