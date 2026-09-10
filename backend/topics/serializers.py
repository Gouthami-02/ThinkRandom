from rest_framework import serializers
from .models import Topic,Favorite


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = [
            'id',
            'question',
            'category',
            'difficulty',
            'topic_type',
        ]
class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = [
            'id',
            'topic',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]