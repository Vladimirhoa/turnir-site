from django.db import models

class Athlete(models.Model):
    
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    birth_date = models.PositiveIntegerField(verbose_name="Дата рождения", null=True, blank=True)
    rating = models.PositiveIntegerField(default=0, verbose_name="Рейтинг игрока")
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        default='M', 
        verbose_name="Пол"
    )
    
    class Meta:
        verbose_name = "Спортсмен"
        verbose_name_plural = "Спортсмены"
        ordering = ['-rating']
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
