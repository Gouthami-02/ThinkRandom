from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Topic
from .serializers import TopicSerializer


@api_view(['GET'])
def random_topic(request):
    topic = Topic.objects.filter(is_active=True).order_by('?').first()

    if not topic:
        return Response(
            {'detail': 'No active topics available.'},
            status=404
        )

    serializer = TopicSerializer(topic)
    return Response(serializer.data)

@api_view(['GET'])
def topic_list(request):
    topics = Topic.objects.filter(is_active=True).order_by('-created_at')

    serializer = TopicSerializer(topics, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def topic_detail(request, pk):
    try:
        topic = Topic.objects.get(pk=pk, is_active=True)
    except Topic.DoesNotExist:
        return Response(
            {'detail': 'Topic not found.'},
            status=404
        )

    serializer = TopicSerializer(topic)
    return Response(serializer.data)

@api_view(['GET'])
def topics_by_category(request, category):
    topics = Topic.objects.filter(
        category__iexact=category,
        is_active=True
    ).order_by('-created_at')

    serializer = TopicSerializer(topics, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def topics_by_difficulty(request, difficulty):
    topics = Topic.objects.filter(
        difficulty__iexact=difficulty,
        is_active=True
    ).order_by('-created_at')

    serializer = TopicSerializer(topics, many=True)

    return Response(serializer.data)