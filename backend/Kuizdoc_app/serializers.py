from rest_framework import serializers
from .models import Documents, QuizQuestions, UserAnswers, UserScores, kuizDocUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
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
        fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password', 'age', 'gender')

    def create(self, validated_data):
        """
        Create and save a new Non-Litigant instance with validated data.

        Args:
            validated_data: Validated data for creating a new Non-Litigant.

        Returns:
            The created Non-Litigant instance.
        """
        non_litigant = kuizDocUser.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            age=validated_data['age'],
            gender=validated_data['gender']
        )
        non_litigant.set_password(validated_data['password'])
        non_litigant.save()
        return non_litigant

class DocumentsSerializer(serializers.ModelSerializer):
    """
    Serializer for Documents model.
    """
    class Meta:
        model = Documents
        fields = '__all__'

class QuizQuestionsSerializer(serializers.ModelSerializer):
    """
    Serializer for QuizQuestions model.
    """
    class Meta:
        model = QuizQuestions
        fields = '__all__'

class UserAnswersSerializer(serializers.ModelSerializer):
    """
    Serializer for UserAnswers model.
    """
    class Meta:
        model = UserAnswers
        fields = '__all__'

class UserScoresSerializer(serializers.ModelSerializer):
    """
    Serializer for UserScores model.
    """
    class Meta:
        model = UserScores
        fields = '__all__'

class UserSerializer(serializers.Serializer):
    """
    Serializer for User model.
    """
    model = User
    fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        """
        Create and save a new User instance with validated data.

        Args:
            validated_data: Validated data for creating a new User.

        Returns:
            The created User instance.
        """
        user = User.objects.create_user(**validated_data)
        return user
