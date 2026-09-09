from django.urls import path
from .views import random_topic,topic_list,topic_detail,topics_by_category,topics_by_difficulty


urlpatterns = [
    path('', topic_list, name='topic-list'),
    path('random/', random_topic, name='random-topic'),
    path('<int:pk>/',topic_detail, name='topic_detail'),   
    path('category/<str:category>/', topics_by_category, name='topics-by-category'),
    path('difficulty/<str:difficulty>/', topics_by_difficulty, name='topics-by-difficulty'),
] 