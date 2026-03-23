from pyexpat.errors import messages
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .forms import FlashcardForm

from django.shortcuts import redirect, render
from .models import Flashcard, UserProgress
# Create your views here.

def index(request):
    return render(request, 'index.html', {
        
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
    
    to_review = UserProgress.objects.filter(user=request.user, next_review__lte=timezone.now()).all()

    return render(request, 'to_review.html', {
        'to_review': to_review
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Create the user
            form.save()
            return redirect('login')
    else:   
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def add_flashcard(request):
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save()
            UserProgress.objects.create(user=request.user, flashcard=flashcard, next_review=timezone.now())
            return redirect('dashboard')
    else:
        form = FlashcardForm()
    return render(request, 'add_flashcard.html', {'form': form})