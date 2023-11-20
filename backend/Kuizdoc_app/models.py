from django.db import models
from django.contrib.auth.models import User as UserAuth

class Documents(models.Model):
    DocumentID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(UserAuth, on_delete=models.CASCADE)
    DocumentText = models.TextField()
    DateCreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'Documents'
        verbose_name_plural = "Documents"

class QuizQuestions(models.Model):
    QuestionID = models.AutoField(primary_key=True)
    DocumentID = models.ForeignKey(Documents, on_delete=models.CASCADE)
    QuestionText = models.TextField()
    OptionA = models.CharField(max_length=200)
    OptionB = models.CharField(max_length=200)
    OptionC = models.CharField(max_length=200)
    OptionD = models.CharField(max_length=200)
    CorrectAnswer = models.CharField(max_length=1)  # Assuming correct answer is a single character (A, B, C, or D)
    DateCreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'QuizQuestions'
        verbose_name_plural = "QuizQuestions"   

class UserAnswers(models.Model):
    AnswerID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(UserAuth, on_delete=models.CASCADE)
    QuestionID = models.ForeignKey(QuizQuestions, on_delete=models.CASCADE)
    UserAnswer = models.CharField(max_length=1)  # Assuming user's answer is a single character (A, B, C, or D)
    DateCreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'UserAnswers'
        verbose_name_plural = "UserAnswers"

class UserScores(models.Model):
    ScoreID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(UserAuth, on_delete=models.CASCADE)
    QuizID = models.ForeignKey(QuizQuestions, on_delete=models.CASCADE)
    Score = models.IntegerField()
    DateCreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'UserScores'
        verbose_name_plural = "UserScores"

