from django.contrib import admin
from .models import Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'question',
        'category',
        'difficulty',
        'topic_type',
        'is_active',
    )

    list_filter = (
        'category',
        'difficulty',
        'topic_type',
        'is_active',
    )

    search_fields = (
        'question',
        'category',
    )
 