from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index, dashboard, start_review, register, add_flashcard

urlpatterns = [
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add_flashcard/', add_flashcard, name='add_flashcard'),
    path('review/', start_review, name='start_review'),
]