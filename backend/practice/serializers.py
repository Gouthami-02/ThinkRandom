from rest_framework import serializers

from .models import PracticeSession


class PracticeSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PracticeSession
        fields = [
            'id',
            'topic',
            'started_at',
            'completed_at',
            'duration_seconds',
            'notes',
            'score',
            'status',
        ]

        read_only_fields = [
            'id',
            'started_at',
            'completed_at',
            'duration_seconds',
            'score',
            'status',
        ]