from rest_framework import serializers
from .models import *

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Emotion
        fields = ['emotion']


class JournalSerializer(serializers.ModelSerializer):
    EmotionalStatus = EmotionSerializer(many= True)

    class Meta:
        model= Journal
        fields = ['id','Note', 'DateTime', 'EmotionalStatus']

    def create(self, validated_data):
        emotional_status_data = validated_data.pop('EmotionalStatus')
        journalnote = Journal.objects.create(**validated_data)
        for emotion_data in emotional_status_data:
            e = Emotion.objects.get(**emotion_data)
            journalnote.EmotionalStatus.add(e)
        return journalnote

    def update(self, instance, validated_data):
        instance.note = validated_data.get('Note', instance.Note)
        instance.dateTime = validated_data.get('DateTime', instance.DateTime)
        Emotional_status_data = validated_data.pop('EmotionalStatus')
        for emotion_data in Emotional_status_data:
            e = Emotion.objects.get(**emotion_data)
            instance.EmotionalStatus.add(e)
        instance.save()
        return instance
