from django.urls import path

from .views import(
     start_practice_session,
     complete_practice_session,
     practice_history,
     topic_history,
     adaptive_challenge,
     speech_analysis,
     generate_speech_analysis,
)


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
    path(
        'history/',
        practice_history,
        name='practice-history'
    ),
    path('topic-history/', topic_history, name='topic-history'),
    path('adaptive-challenge/', adaptive_challenge, name='adaptive-challenge'),
    path(
    'sessions/<int:session_id>/analysis/',
    speech_analysis,
    name='speech-analysis'
    ),
    path(
    'sessions/<int:session_id>/analyze/',
    generate_speech_analysis,
    name='generate-speech-analysis'
    ),
]