from django import forms

from django.forms import ModelForm
from .models import Tournament, News

class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ["name", "description", "regulations", "start_date", "end_date"]

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название турнира'}),
            'description': forms.Textarea(attrs={'placeholder': 'Описания турнира'}),
            'regulations': forms.Textarea(attrs={'placeholder': 'Регламент'}),
            'start_date': forms.TextInput(attrs={'placeholder': 'Пример: 23.10.2023'}),
            'end_date': forms.TextInput(attrs={'placeholder': 'Пример: 23.10.2023'}),
        }
