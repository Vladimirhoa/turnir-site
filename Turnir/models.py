from django.db import models
from Athlete.models import Athlete 
from django.db import transaction
from django.db.models import Q  # Обязательно импортируем Q для сложных запросов

class League(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название лиги (Хард, Лайт и т.д.)")
    points_1 = models.PositiveIntegerField(verbose_name="Очки за 1 место", default=0)
    points_2 = models.PositiveIntegerField(verbose_name="Очки за 2 место", default=0)
    points_3 = models.PositiveIntegerField(verbose_name="Очки за 3 место", default=0)
    points_4 = models.PositiveIntegerField(verbose_name="Очки за 4 место", default=0)
    points_other = models.PositiveIntegerField(verbose_name="Очки остальным", default=0)

    class Meta:
        verbose_name = "Лига"
        verbose_name_plural = "Лиги"

    def __str__(self):
        return self.name

class Tournament(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('MIX', 'Микст (М+Ж)'),
        ('ANY', 'Любой'),
    ]
    name = models.CharField(max_length=100, verbose_name="Название турнира")
    date = models.DateField(verbose_name="Дата проведения")
    start_time = models.TimeField(verbose_name="Время начала", null=True, blank=True)
    end_time = models.TimeField(verbose_name="Время окончания", null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name="Адрес проведения", null=True, blank=True)
    is_finished = models.BooleanField(default=False, verbose_name="Турнир завершен (очки начислены)")
    birth_year_from = models.PositiveIntegerField(verbose_name="Год рождения от", null=True, blank=True)
    birth_year_to = models.PositiveIntegerField(verbose_name="Год рождения до", null=True, blank=True)
    allowed_gender = models.CharField(max_length=3, choices=GENDER_CHOICES, default='ANY', verbose_name="Допустимый пол")

    def __str__(self):
        return f"{self.name} ({self.date})"
        
    def get_age_category_display(self):
        if self.birth_year_from and self.birth_year_to:
            return f"{self.birth_year_from}-{self.birth_year_to}"
        elif self.birth_year_from:
            return f"от {self.birth_year_from} г.р."
        elif self.birth_year_to:
            return f"до {self.birth_year_to} г.р."
        return "Без ограничений"

    def save(self, *args, **kwargs):
        status_changed = False

        if self.pk:
            old_instance = Tournament.objects.get(pk=self.pk)
            if old_instance.is_finished != self.is_finished:
                status_changed = True
        else:
            if self.is_finished:
                status_changed = True

        super().save(*args, **kwargs)

        if status_changed:
            self.recalculate_athletes_rating()

    def recalculate_athletes_rating(self):
        """Полный пересчет рейтинга с нуля для всех участников турнира"""
        athletes = set()
        for team in self.team_set.select_related('player_1', 'player_2'):
            athletes.add(team.player_1)
            athletes.add(team.player_2)

        with transaction.atomic():
            for athlete in athletes:
                finished_teams = Team.objects.filter(
                    Q(player_1=athlete) | Q(player_2=athlete),
                    tournament__is_finished=True
                ).select_related('league')

                # 3. Считаем сумму очков заново
                total_points = sum(team.earned_points for team in finished_teams)
                
                # 4. Обновляем рейтинг в БД
                athlete.rating = total_points
                athlete.save(update_fields=['rating'])


class Team(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, verbose_name="Турнир")
    league = models.ForeignKey(League, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Лига")
    player_1 = models.ForeignKey(Athlete, on_delete=models.PROTECT, related_name='teams_p1', verbose_name="Игрок 1")
    player_2 = models.ForeignKey(Athlete, on_delete=models.PROTECT, related_name='teams_p2', verbose_name="Игрок 2")
    place = models.PositiveIntegerField(verbose_name="Итоговое место в турнире", null=True, blank=True)
    

    
    @property
    def earned_points(self):
        if not self.place or not self.league: 
            return 0 
        
        if self.place == 1: return self.league.points_1
        elif self.place == 2: return self.league.points_2
        elif self.place == 3: return self.league.points_3
        elif self.place == 4: return self.league.points_4
        else: return self.league.points_other

    def __str__(self):
        league_name = self.league.name if self.league else "Квал."
        return f"[{league_name}] {self.player_1.last_name} / {self.player_2.last_name}"
    
class Match(models.Model): 
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, verbose_name="Турнир")
    
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team1', verbose_name="Команда 1")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team2', verbose_name="Команда 2")
    
    referee = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='matches_as_referee', null=True, blank=True, verbose_name="Судит")
    

    stage = models.CharField(max_length=50, verbose_name="Стадия турнира", blank=True)
    is_finished = models.BooleanField(default=False, verbose_name="Матч завершен")

    court = models.PositiveIntegerField(verbose_name="Корт", null=True, blank=True)
    team1_score = models.PositiveIntegerField(verbose_name="Счет команды 1", null=True, blank=True)
    team2_score = models.PositiveIntegerField(verbose_name="Счет команды 2", null=True, blank=True)

    class Meta:
        verbose_name = "Матч"
        verbose_name_plural = "Матчи"
        ordering = ['is_finished', 'court']

    def __str__(self):
        stage_str = f" [{self.stage}]" if self.stage else ""
        return f"{self.team1} - {self.team2}{stage_str}"

    @property
    def who_win(self):
        if self.team1_score is None or self.team2_score is None:
            return None
            
        if self.team1_score > self.team2_score:
            return self.team1
        elif self.team1_score < self.team2_score:
            return self.team2
        else:
            return None 
