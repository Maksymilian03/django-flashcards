from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Flashcard(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question
    
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bin = models.IntegerField(default=0)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    next_review = models.DateTimeField(default=timezone.now)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'flashcard')

    def __str__(self):
        return f"{self.user.username} - {self.flashcard.question} (Bin {self.bin})"
