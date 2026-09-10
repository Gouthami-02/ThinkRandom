from django.urls import path

from .views import start_practice_session,complete_practice_session


urlpatterns = [
    path(
        'sessions/',
        start_practice_session,
        name='start-practice-session'
    ),
    path(
        'sessions/<int:pk>/complete/',
        complete_practice_session,
        name='complete-practice-session'
    ),
]