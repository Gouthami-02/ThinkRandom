from django.urls import path

from .views import (
    random_topic,
    topic_list,
    topic_detail,
    topics_by_category,
    topics_by_difficulty,
    add_favorite,
    remove_favorite,
    favorite_list,
)


urlpatterns = [
    path('', topic_list, name='topic-list'),

    path(
        'random/',
        random_topic,
        name='random-topic'
    ),

    path(
        '<int:pk>/',
        topic_detail,
        name='topic-detail'
    ),

    path(
        'category/<str:category>/',
        topics_by_category,
        name='topics-by-category'
    ),

    path(
        'difficulty/<str:difficulty>/',
        topics_by_difficulty,
        name='topics-by-difficulty'
    ),

    path(
        'favorites/',
        favorite_list,
        name='favorite-list'
    ),

    path(
        '<int:pk>/favorite/',
        add_favorite,
        name='add-favorite'
    ),

    path(
        '<int:pk>/favorite/remove/',
        remove_favorite,
        name='remove-favorite'
    ),
]