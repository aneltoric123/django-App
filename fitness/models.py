from datetime import timezone
from tkinter.constants import CASCADE

from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField


# Create your models here.

class UserProfile(models.Model):
    GOAL_CHOICES = [
        ('lose_weight', 'Lose Weight'),
        ('gain_muscle', 'Gain Muscle'),
        ('improve_health', 'Improve Health'),
        ('maintain', 'Maintain Weight'),
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    country = CountryField(blank_label='Select a country')
    current_weight = models.FloatField(blank=True)
    goal = models.CharField(max_length=20,choices=GOAL_CHOICES,blank=True)

    def is_complete(self):
        return all([
            self.age,
            self.country,
            self.current_weight,
            self.goal
        ])

class WeightEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.weight} kg on {self.date}"
