from rest_framework import serializers
from .models import Documents, QuizQuestions, UserAnswers, UserScores, User 
from django.contrib.auth.models import User


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

class UserSerializer(serializers.Serializer):
    model = User
    fields = ['first_name', 'last_name', 'email', 'Password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user