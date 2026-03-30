from pyexpat.errors import messages
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .forms import FlashcardForm

from django.shortcuts import get_object_or_404, redirect, render
from .models import Flashcard, UserProgress
# Create your views here.

def index(request):
    return render(request, 'index.html', {
        
    })
@login_required
def dashboard(request):

    to_learn = UserProgress.objects.filter(user=request.user, bin__lt=6).count()

    flashcards_learned =UserProgress.objects.filter(user=request.user, bin=6).count()

    to_review = UserProgress.objects.filter(user=request.user, next_review__date__lte=timezone.now().date(), bin__lt=6).count()

    return render(request, 'dashboard.html', {
        'to_learn': to_learn,
        'flashcards_learned': flashcards_learned,
        'to_review': to_review
    })

@login_required

def start_review(request):
    
    to_review = UserProgress.objects.filter(user=request.user, next_review__date__lte=timezone.now().date(), bin__lt=6).all()

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

@login_required
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


@login_required
def mark_flashcard(request, progress_id, correct):
    progress = get_object_or_404(UserProgress, id=progress_id, user=request.user)

    data_now = timezone.now()

    if correct == 'true':
        if progress.bin == 0:
            days_to_add = 1
        elif progress.bin == 1:
            days_to_add = 3         
        elif progress.bin == 2:
            days_to_add = 7
        elif progress.bin == 3:
            days_to_add = 14
        elif progress.bin == 4:
            days_to_add = 30
        elif progress.bin == 5:
            days_to_add = 1
        
        progress.bin += 1
        progress.next_review = data_now + timezone.timedelta(days=days_to_add)
    
    else:
        progress.next_review = data_now + timezone.timedelta(days=1)
    
    progress.last_reviewed = data_now
    progress.save()

    return redirect('start_review')
    