from django.db import models
from django.contrib.auth.models import User

from topics.models import Topic


class PracticeSession(models.Model):
    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Abandoned', 'Abandoned'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='practice_sessions'
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='practice_sessions'
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    duration_seconds = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    score = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='In Progress'
    )

    def __str__(self):
        return f"{self.user.username} - {self.topic.question[:50]}"

class TopicHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='topic_history'
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='history_records'
    )

    viewed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.topic.question[:50]}"
