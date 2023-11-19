from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nameUser = models.CharField(max_length=100, default='Inkognit', null=True)
    registered_tournaments = models.ManyToManyField('Tournament', through='TournamentTable')
    def __str__(self):
        return self.nameUser

class Tournament(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    regulations = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()


class TournamentTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nameUser = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    team = models.CharField(max_length=30)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    matches_played = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    goals_for = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)
    goals_difference = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
