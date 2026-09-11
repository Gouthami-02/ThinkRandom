from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from .models import Topic,Favorite
from .serializers import TopicSerializer,FavoriteSerializer

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request, pk):

    try:
        topic = Topic.objects.get(
            id=pk,
            is_active=True
        ) 
    except Topic.DoesNotExist:
        return Response(
            {'detail': 'Topic not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        topic=topic
    )

    if not created:
        return Response(
            {'detail': 'Topic is already in favorites.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = FavoriteSerializer(favorite)

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favorite(request, pk):

    try:
        favorite = Favorite.objects.get(
            user=request.user,
            topic_id=pk
        )
    except Favorite.DoesNotExist:
        return Response(
            {'detail': 'Favorite not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    favorite.delete()

    return Response(
        {'message': 'Topic removed from favorites.'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_list(request):

    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related('topic').order_by('-created_at')

    serializer = FavoriteSerializer(
        favorites,
        many=True
    )

    return Response(serializer.data)