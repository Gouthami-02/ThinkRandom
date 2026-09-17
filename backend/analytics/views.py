from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from practice.models import PracticeSession
from django.db.models import Avg

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):

    sessions = PracticeSession.objects.filter(
        user=request.user
    )

    completed_sessions = sessions.filter(
        status='Completed'
    )

    total_practices = sessions.count()

    completed_count = completed_sessions.count()

    average_score = 0

    scored_sessions = completed_sessions.filter(
        score__isnull=False
    )

    if scored_sessions.exists():
        total_score = sum(
            session.score for session in scored_sessions
        )
        average_score = round(
            total_score / scored_sessions.count(),
            2
        )
    category_performance = (
        completed_sessions
        .filter(score__isnull=False)
        .values('topic__category')
        .annotate(average_score=Avg('score'))
        .order_by('-average_score')
    )
    weakest_category = (
        completed_sessions
        .filter(score__isnull=False)
        .values('topic__category')
        .annotate(average_score=Avg('score'))
        .order_by('average_score')
        .first()
  )

    return Response({
        'total_practices': total_practices,
        'completed_practices': completed_count,
        'average_score': average_score,
        'category_performance': [{
            'category': item['topic__category'],
            'average_score': round(item['average_score'], 2),
        }
        for item in category_performance
        ],
        'weakest_category': ({
            'category': weakest_category['topic__category'],
            'average_score': round(weakest_category['average_score'], 2),
        }
         if weakest_category
         else None
        ),
    })
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def progress(request):

    sessions = PracticeSession.objects.filter(
        user=request.user
    )

    completed_sessions = sessions.filter(
        status='Completed'
    )

    scored_sessions = completed_sessions.filter(
        score__isnull=False
    )

    total_practices = sessions.count()
    completed_count = completed_sessions.count()

    average_score = 0
    best_score = 0

    if scored_sessions.exists():

        scores = [
            session.score
            for session in scored_sessions
        ]

        average_score = round(
            sum(scores) / len(scores),
            2
        )

        best_score = max(scores)

    recent_activity = (
        completed_sessions
        .select_related('topic')
        .order_by('-completed_at')[:5]
    )

    return Response({
        'total_practices': total_practices,
        'completed_practices': completed_count,
        'average_score': average_score,
        'best_score': best_score,
        'recent_activity': [
            {
                'session_id': session.id,
                'topic': session.topic.question,
                'category': session.topic.category,
                'score': session.score,
                'completed_at': session.completed_at,
            }
            for session in recent_activity
        ],
    })