from django.db import models

from journal.models import Emotion
from meditation.models import Course, Track
from user.models import User

# Create your models here.

class meditation_session(models.Model):
    dateTime = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, related_name='meditation_course_sessions')
    track = models.ForeignKey(Track, on_delete=models.DO_NOTHING, related_name='sessions')
    duration = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meditation_sessions')
    startingEmotion = models.ForeignKey(Emotion, on_delete=models.DO_NOTHING, related_name='initial_emotion')
    endingingEmotion = models.ForeignKey(Emotion, on_delete=models.DO_NOTHING, related_name='final_emotion')