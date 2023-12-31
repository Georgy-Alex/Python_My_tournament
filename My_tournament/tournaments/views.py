from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Tournament, News, UserProfile, TournamentTable
from .forms import TournamentForm, NewsTournamentForm, RegistrationTeamTournamentForm, UserProfileForm, \
    EditTableTournamentForm
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'tournaments/home.html')


# РЕГИСТРАЦИЯ

def registration(request):
    if request.method == 'GET':
        return render(request, 'tournaments/registration.html',
                      {'Login_form': UserCreationForm(), 'Name_form': UserProfileForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                form = UserProfileForm(request.POST)
                new_user = form.save(commit=False)
                new_user.user = request.user
                new_user.save()
                return redirect('home')
            except IntegrityError:
                return render(request, 'tournaments/registration.html',
                              {'Login_form': UserCreationForm(), 'Name_form': UserProfileForm(),
                               'error': 'имя пользователя уже используется'})
        else:
            return render(request, 'tournaments/registration.html',
                          {'form': UserCreationForm(), 'error': 'Пароль неверный'})


def authorization(request):
    if request.method == 'GET':
        return render(request, 'tournaments/authorization.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'tournaments/authorization.html',
                          {'form': AuthenticationForm(), 'error': 'Неверный данные'})
        else:
            login(request, user)
            return redirect('home')


def logoutUser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


# ТУРНИР

@login_required
def tournaments(request):
    tournams = Tournament.objects.all()

    return render(request, 'tournaments/tournaments.html', {'tournams': tournams})


@login_required
def my_Tournaments(request):
    tournams = Tournament.objects.filter(user=request.user)
    return render(request, 'tournaments/myTournaments.html', {'tournams': tournams})

def myRegTournam(request):
    userProfile = UserProfile.objects.get(user=request.user)
    tournams = userProfile.registered_tournaments.all()
    return render(request, 'tournaments/myRegistrationTournam.html', {'tournams': tournams})

flag = False


def trueORfalse(request, tournam_id):
    global flag
    flag = True if flag == False else False
    if request.method == 'POST':
        return redirect('tournam', tournam_id=tournam_id)


def tournam(request, tournam_id):
    userProfile = UserProfile.objects.get(user=request.user)
    my_tournam = Tournament.objects.filter(user=request.user)
    tournam = get_object_or_404(Tournament, pk=tournam_id)
    flagBlock = userProfile not in tournam.blocked_users.all()
    tournam_table = TournamentTable.objects.filter(tournament=tournam).order_by('-points')
    flagTeam = tournam.total_teams != len(tournam_table)
    news = News.objects.filter(tournament=tournam)


    return render(request, 'tournaments/tournam.html',
                  {'tournam': tournam, 'form': RegistrationTeamTournamentForm(), 'news': news,
                   'tournam_table': tournam_table, 'my_tournam': my_tournam,
                   'flagBlock': flagBlock, 'flagTeam': flagTeam, 'flag': flag})


@login_required
def addTournament(request):
    if request.method == 'GET':
        return render(request, 'tournaments/addTournament.html', {'form': TournamentForm()})
    else:
        try:
            form = TournamentForm(request.POST)
            new_prod = form.save(commit=False)
            new_prod.user = request.user
            new_prod.save()
            return redirect('home')
        except ValueError:
            return render(request, 'tournaments/addTournament.html',
                          {'form': TournamentForm(), 'error': 'Неверный данные'})


def editTournam(request, tournam_id):
    tournam = get_object_or_404(Tournament, pk=tournam_id)
    form = TournamentForm(instance=tournam)
    if request.method == 'GET':
        return render(request, 'tournaments/editTournam.html', {'tournam': tournam,
                                                                'form': form})
    else:
        try:
            form = TournamentForm(request.POST, instance=tournam)
            form.save()
            return redirect('my_Tournaments')
        except ValueError:
            return render(request, 'tournaments/editTournam.html', {'tournam': tournam,
                                                                    'form': form,
                                                                    'error': 'Неверные данные'})

@login_required
def deletetournam(request, tournam_id):
    tournam = get_object_or_404(Tournament, pk=tournam_id, user=request.user)
    if request.method == 'POST':
        tournam.delete()
        return redirect('tournaments')

# ТАБЛИЦА

def registTeam(request, tournam_id):
    tournament = Tournament.objects.get(pk=tournam_id)
    userProfile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            form = RegistrationTeamTournamentForm(request.POST)
            new_team = form.save(commit=False)
            new_team.user = request.user
            new_team.tournament = tournament
            new_team.nameUser = userProfile
            new_team.save()
            userProfile.registered_tournaments.add(tournament)
            global flag
            flag = False
            return redirect('tournam', tournam_id=tournam_id)
        except ValueError:
            return render(request, 'tournaments/tournam.html',
                          {'form': RegistrationTeamTournamentForm(), 'error': 'Неверный данные'})


def editTable(request, tournam_id):
    tournam = get_object_or_404(Tournament, pk=tournam_id)
    tournam_table = TournamentTable.objects.filter(tournament=tournam).order_by('-points')
    form = []
    for team in tournam_table:
        form.append(EditTableTournamentForm(instance=team, prefix=team.id))
    if request.method == 'GET':
        return render(request, 'tournaments/editTableTournam.html', {'tournam_table': tournam_table,
                                                                     'form': form})
    else:
        try:
            for team in tournam_table:
                form_team = EditTableTournamentForm(request.POST, instance=team, prefix=team.id)
                form_team.save()
            return redirect('tournam', tournam_id=tournam_id)
        except ValueError:
            return render(request, 'tournaments/editTableTournam.html', {'tournam_table': tournam_table,
                                                                         'form': form,
                                                                         'error': 'Неверные данные'})
def blockUser(request, team_id):
    team = get_object_or_404(TournamentTable, pk=team_id)
    if request.method == 'GET':
        team.tournament.blocked_users.add(team.nameUser)
        return redirect('tournam', tournam_id=team.tournament.id)

def deletetTableTeam(request, team_id):
    team = get_object_or_404(TournamentTable, pk=team_id)
    if request.method == 'GET':
        team.delete()
        return redirect('tournaments')

# Новости

def new(request, new_id):
    new = get_object_or_404(News, pk=new_id)
    return render(request, 'tournaments/newPage.html', {'new': new})


def addNews(request, tournam_id):
    tournament = Tournament.objects.get(pk=tournam_id)

    if request.method == 'GET':
        return render(request, 'tournaments/addNews.html', {'form': NewsTournamentForm()})

    else:
        try:
            form = NewsTournamentForm(request.POST)
            new_news = form.save(commit=False)
            new_news.user = request.user
            new_news.tournament = tournament
            new_news.save()
            return redirect('tournam', tournam_id=tournam_id)
        except ValueError:
            return render(request, 'tournaments/addNews.html',
                          {'form': NewsTournamentForm(), 'error': 'Неверный данные'})


def deletetNew(request, new_id, tournam_id):
    new = get_object_or_404(News, pk=new_id, user=request.user)
    if request.method == 'POST':
        new.delete()
        return redirect('tournam', tournam_id=tournam_id)
