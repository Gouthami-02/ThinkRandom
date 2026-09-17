from django.urls import path

from .views import dashboard, progress


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('progress/', progress, name='progress'),

]