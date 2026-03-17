from django.urls import path
from .views import index, dashboard, start_review

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('review/', start_review, name='start_review'),
]