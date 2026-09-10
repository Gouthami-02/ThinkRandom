from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from topics.models import Topic

from .models import PracticeSession
from .serializers import PracticeSessionSerializer


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