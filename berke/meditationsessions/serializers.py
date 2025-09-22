from rest_framework import serializers
from journal.models import Emotion
from meditation.serializers import CourseSerializer, TrackSerializer
from journal.serializers import EmotionSerializer
from .models import meditation_session


class MeditationSessionSerializer(serializers.ModelSerializer):
    initialEmotion = EmotionSerializer(source='initial_emotion')
    finalEmotion = EmotionSerializer(source='final_emotion')
    course = CourseSerializer(source='course')
    track = TrackSerializer(source = 'track')

    class Meta:
        model= meditation_session
        fields = ['dateTime', 'course', 'track', 'duration', 'initialEmotion', 'finalEmotion']

    def create(self, validated_data):
        initial_emotion_data = validated_data.pop('initialEmotion')
        final_emotion_data = validated_data.pop('finalEmotion')
        new_meditation_session = meditation_session.objects.create(**validated_data)
        new_meditation_session.initial_emotion = initial_emotion_data
        new_meditation_session.final_emotion = final_emotion_data
        new_meditation_session.save()
        return new_meditation_session


class JourneyListSerializer(serializers.ModelSerializer):
    trackId = serializers.IntegerField(source="track.id")
    courseId = serializers.IntegerField(source="course.id")

    class Meta:
        model = meditation_session
        fields = ["id", "courseId", "trackId"]