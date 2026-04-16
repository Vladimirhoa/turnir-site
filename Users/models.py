from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class Users(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.CharField(unique=True) 
    rating = models.PositiveIntegerField(default=0, verbose_name="Рейтинг игрока")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    current_year = datetime.date.today().year
    birth_date = models.PositiveIntegerField(verbose_name="Дата рождения", null=True, blank=True, 
        validators=[
            MinValueValidator(1930, message="Год рождения не может быть меньше 1930."),
            MaxValueValidator(current_year, message="Год рождения не может быть больше текущего.")
        ]
    )
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['first_name', 'last_name'] 

    objects = CustomUserManager()

    def __str__(self):
        return self.email