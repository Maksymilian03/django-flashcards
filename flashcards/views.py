from django.utils import timezone

from django.shortcuts import render
from .models import Flashcard, UserProgress
# Create your views here.

def index(request):
    return render(request, 'index.html', {
        'flashcards': Flashcard.objects.all(),
        'progress': UserProgress.objects.filter(user=request.user)
    })

def dashboard(request):
    stats = []

    for i in range (1, 6):
        stats.append({
            'bin': i,
            'count': UserProgress.objects.filter(user=request.user, bin=i).count()
        })
    
    to_review = UserProgress.objects.filter(user=request.user, next_review__lte=timezone.now()).count()

    return render(request, 'dashboard.html', {
        'stats': stats,
        'to_review': to_review
    })

def start_review(request):
    print(f"Starting review - {timezone.now()}")
    to_review = UserProgress.objects.filter(user=request.user, next_review__lte=timezone.now()).first()

    return render(request, 'to_review.html', {
        'to_review': to_review
    })