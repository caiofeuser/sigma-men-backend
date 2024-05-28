from rest_framework import serializers
from .models import (
    Survey,
    Question,
    Track,
    Option,
    Result
)


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'question', 'position', 'survey', 'options')


class ResultSerializer(serializers.ModelSerializer):
    survey = SurveySerializer()
    track = TrackSerializer()

    class Meta:
        model = Result
        fields = ('id', 'survey', 'track')
