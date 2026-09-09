from django.contrib import admin
from .models import PracticeSession


@admin.register(PracticeSession)
class PracticeSessionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'topic',
        'status',
        'score',
        'started_at',
        'completed_at',
        'duration_seconds',
    )

    list_filter = (
        'status',
        'score',
        'started_at',
    )

    search_fields = (
        'user__username',
        'topic__question',
    )