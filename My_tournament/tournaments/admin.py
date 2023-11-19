from django.contrib import admin
from .models import Tournament, News, UserProfile, TournamentTable

admin.site.register(Tournament)
admin.site.register(News)
admin.site.register(UserProfile)
admin.site.register(TournamentTable)
