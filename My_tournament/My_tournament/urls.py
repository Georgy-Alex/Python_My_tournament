"""
URL configuration for My_tournament project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tournaments import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # Авторизация
    path('regist/', views.registration, name='registration'),
    path('authoriz/', views.authorization, name='authorization'),
    path('logout/', views.logoutUser, name='logoutUser'),

    # Турниры
    path('my_Tournaments/', views.my_Tournaments, name='my_Tournaments'),
    path('addTournament/', views.addTournament, name='addTournament'),
    path('edittournaments/<int:tournam_id>', views.editTournam, name='editTournam'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('tournam/<int:tournam_id>', views.tournam, name='tournam'),

    path('tournament/<int:tournam_id>/delete', views.deletetournam, name='deletetournam'),

    # Новости
    path('new/<int:new_id>', views.new, name='new'),
    path('tournament/<int:tournam_id>/add_news/', views.addNews, name='addNews'),
    path('deletetNew/<int:new_id>/<int:tournam_id>', views.deletetNew, name='deletetNew'),

    # Таблица

    path('trueORFalse/<int:tournam_id>', views.trueORfalse, name='trueORFalse'),
    path('registrationTeam/<int:tournam_id>', views.registTeam, name='registTeam'),

]
