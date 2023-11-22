from rest_framework import serializers
from .models import Documents, QuizQuestions, UserAnswers, UserScores

class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'


class QuizQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestions
        fields = '__all__'


class UserAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswers
        fields = '__all__'


class UserScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScores
        fields = '__all__'