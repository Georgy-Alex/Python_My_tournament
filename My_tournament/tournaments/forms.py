from django import forms

from django.forms import ModelForm
from .models import Tournament, News, TournamentTable, UserProfile

class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ["name", "email", "description", "regulations", "total_teams", "start_date", "end_date"]

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название турнира'}),
            'email': forms.Textarea(attrs={'placeholder': 'Ваш email'}),
            'description': forms.Textarea(attrs={'placeholder': 'Описания турнира'}),
            'regulations': forms.Textarea(attrs={'placeholder': 'Регламент'}),
            'total_teams': forms.Textarea(attrs={'placeholder': 'Количество команд'}),
            'start_date': forms.TextInput(attrs={'placeholder': 'Пример: 23.10.2023'}),
            'end_date': forms.TextInput(attrs={'placeholder': 'Пример: 23.10.2023'}),
        }

class NewsTournamentForm(ModelForm):
    class Meta:
        model = News
        fields = ["title", "content"]

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название новости'}),
            'content': forms.Textarea(attrs={'placeholder': 'Контент новости'}),
        }

class RegistrationTeamTournamentForm(ModelForm):
    class Meta:
        model = TournamentTable
        fields = ["team"]

        widgets = {
            'team': forms.TextInput(attrs={'placeholder': 'Название команды'}),
        }

class EditTableTournamentForm(ModelForm):
    class Meta:
        model = TournamentTable
        fields = ["team", "matches_played", "wins", "draws", "losses", "goals_for", "goals_against", "goals_difference", "points"]

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nameUser"]

        widgets = {
            'nameUser': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
        }


