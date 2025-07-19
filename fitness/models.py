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
