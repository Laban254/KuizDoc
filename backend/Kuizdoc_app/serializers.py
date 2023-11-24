from rest_framework import serializers
from .models import Documents, QuizQuestions, UserAnswers, UserScores, User, kuizDocUser 
from django.contrib.auth.models import User

# test

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer to add custom claims like 'email' to the token.
    """
    @classmethod
    def get_token(cls, user):
        """
        Override the get_token method to add custom claims to the token.

        Args:
            user: The user for whom the token is generated.

        Returns:
            The JWT token with custom claims.
        """
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['email'] = user.email
        return token

class kuizDocUserSerializer(serializers.ModelSerializer):
    """
    Serializer for Non-Litigant registration and data validation.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = kuizDocUser
        fields = ('first_name', 'first_name', 'email', 'password', 'confirm_password', 'age', 'gender')

    def create(self, validated_data):
        """
        Create and save a new Non-Litigant instance with validated data.

        Args:
            validated_data: Validated data for creating a new Non-Litigant.

        Returns:
            The created Non-Litigant instance.
        """
        non_litigant = kuizDocUser.objects.create(
            
            email=validated_data['email'],
        )
        non_litigant.set_password(validated_data['password'])
        non_litigant.save()
        return non_litigant



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