from django.db import models

from user.models import User

# Create your models here.

class Journal(models.Model):
    dateTime = models.DateTimeField()
    note = models.TextField()
    emotionalStatus = models.ManyToManyField("Emotion", related_name="Mood")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal')
    def __str__(self):
        return (self.note)
    


class Emotion(models.Model):
    emotion = models.CharField(max_length=32)
    def __str__(self):
        return (self.emotion)