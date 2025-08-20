from django.db import models

# Create your models here.

class Tag(models.Model):
    title = models.CharField(max_length=64)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=64)
    tags = models.ManyToManyField(Tag)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Track(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tracks')
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    audio_url = models.URLField()
    duration = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title