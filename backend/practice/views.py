import random
from django.utils import timezone
from django.db.models import Avg

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from topics.models import Topic
from topics.serializers import TopicSerializer

from .models import PracticeSession, TopicHistory
from .serializers import PracticeSessionSerializer, TopicHistorySerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_practice_session(request):

    topic_id = request.data.get('topic')

    if not topic_id:
        return Response(
            {'detail': 'Topic is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        topic = Topic.objects.get(
            id=topic_id,
            is_active=True
        )
    except Topic.DoesNotExist:
        return Response(
            {'detail': 'Topic not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    session = PracticeSession.objects.create(
        user=request.user,
        topic=topic
    )
    TopicHistory.objects.create(
        user=request.user,
        topic=topic
    )

    serializer = PracticeSessionSerializer(session)

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def complete_practice_session(request, pk):

    try:
        session = PracticeSession.objects.get(
            id=pk,
            user=request.user
        )
    except PracticeSession.DoesNotExist:
        return Response(
            {'detail': 'Practice session not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if session.status != 'In Progress':
        return Response(
            {'detail': 'Practice session is already completed or abandoned.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    duration_seconds = request.data.get('duration_seconds')
    notes = request.data.get('notes', '')
    score = request.data.get('score')

    if duration_seconds is None:
        return Response(
            {'detail': 'Duration is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        duration_seconds = int(duration_seconds)
    except (TypeError, ValueError):
        return Response(
            {'detail': 'Duration must be a valid number.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if duration_seconds < 0:
        return Response(
            {'detail': 'Duration cannot be negative.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if score is not None:
        try:
            score = int(score)
        except (TypeError, ValueError):
            return Response(
                {'detail': 'Score must be a valid number.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if score < 0 or score > 100:
            return Response(
                {'detail': 'Score must be between 0 and 100.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    session.duration_seconds = duration_seconds
    session.notes = notes
    session.score = score
    session.status = 'Completed'
    session.completed_at = timezone.now()

    session.save()

    serializer = PracticeSessionSerializer(session)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def practice_history(request):

    sessions = PracticeSession.objects.filter(
        user=request.user
    ).order_by('-started_at')

    serializer = PracticeSessionSerializer(
        sessions,
        many=True
    )

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def topic_history(request):
    history = TopicHistory.objects.filter(
        user=request.user
    ).select_related('topic').order_by('-viewed_at')

    serializer = TopicHistorySerializer(
        history,
        many=True
    )

    return Response(serializer.data)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def adaptive_challenge(request):

    completed_sessions = PracticeSession.objects.filter(
        user=request.user,
        status='Completed',
        score__isnull=False
    )
    user_interests = request.user.profile.interests

    weakest_category = (
        completed_sessions
        .values('topic__category')
        .annotate(average_score=Avg('score'))
        .order_by('average_score')
        .first()
    )

    if weakest_category:
        weakest_category_name = weakest_category['topic__category']
        average_score = weakest_category['average_score']

        if average_score >= 80:
            target_difficulty = 'Hard'
        elif average_score >= 60:
            target_difficulty = 'Medium'
        else:
            target_difficulty = 'Easy'
    else:
        weakest_category_name = None
        average_score = None
        target_difficulty = 'Medium'

    profile = getattr(request.user, 'profile', None)

    if profile:
        user_interests = profile.interests or []
    else:
        user_interests = []


    recent_topic_ids = set(
       TopicHistory.objects.filter(
         user=request.user
       ).values_list(
         'topic_id',
          flat=True
       )
   )


    candidate_topics = Topic.objects.filter(
        is_active=True
    )


    best_topic = None
    best_score = -1

    for topic in candidate_topics:

        # 30% - Weakness
        if weakest_category_name:
          weakness_score = (
            1.0
            if topic.category == weakest_category_name
            else 0.0
         )
        else:
           weakness_score = 0.5

         # 25% - Difficulty progression
        difficulty_score = (
           1.0
           if topic.difficulty == target_difficulty
           else 0.0
        )

         # 20% - User interests
        interest_score = (
          1.0
          if topic.category in user_interests
          else 0.0
        )

          # 15% - Topic freshness
        freshness_score = (
           1.0
           if topic.id not in recent_topic_ids
           else 0.0
        )

         # 10% - Randomness
        randomness_score = random.random()

        total_score = (
             weakness_score * 0.30
             + difficulty_score * 0.25
             + interest_score * 0.20
             + freshness_score * 0.15
            + randomness_score * 0.10
        )

        if total_score > best_score:
           best_score = total_score
           best_topic = topic


    topic = best_topic
    selection_score = round(best_score, 3)

   

    topic = candidate_topics.order_by('?').first()

    if not topic:
        return Response(
            {'detail': 'No suitable challenge available.'},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response({
        'topic': TopicSerializer(topic).data,
        'adaptive_score': selection_score,
        'reason': {
            'weakest_category': weakest_category_name,
            'target_difficulty': target_difficulty,
            'user_interests': user_interests,

            'strategy': 'Targeting your weakest category with difficulty progression and topic freshness'
        }
    })