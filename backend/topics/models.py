from django.db import models


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
