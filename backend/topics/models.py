from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    TOPIC_TYPE_CHOICES = [
        ('General', 'General'),
        ('Debate', 'Debate'),
        ('Opinion', 'Opinion'),
        ('Scenario', 'Scenario'),
        ('Creative', 'Creative'),
    ]

    question = models.TextField()

    category = models.CharField(
        max_length=100
    )

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='Medium'
    )

    topic_type = models.CharField(
        max_length=20,
        choices=TOPIC_TYPE_CHOICES,
        default='General'
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.question

class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_topics'
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'topic'],
                name='unique_user_topic_favorite'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.topic.question[:50]}"
