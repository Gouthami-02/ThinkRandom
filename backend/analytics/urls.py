from django.urls import path

from .views import dashboard, progress, leaderboard


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('progress/', progress, name='progress'),
    path('leaderboard/', leaderboard, name='leaderboard'),
]  