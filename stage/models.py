from django.db import models

class stage(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название стадии турнира")
    