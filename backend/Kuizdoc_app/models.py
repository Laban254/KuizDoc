from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager

class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    Password = models.CharField(max_length=200)

    class Meta:
        managed = True
        db_table = 'User'
        verbose_name_plural = "User"

class Documents(models.Model):
    Documentid = models.AutoField(primary_key=True)
    #User = models.ForeignKey(UserAuth, on_delete=models.CASCADE)
    DateCreated = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='documents/')
    #url = models.CharField(max_length=200)
    

    class Meta:
        managed = True
        db_table = 'Documents'
        verbose_name_plural = "Documents"

class QuizQuestions(models.Model):
    Questionid= models.AutoField(primary_key=True)
    Document = models.ForeignKey(Documents, on_delete=models.CASCADE)
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
    Answerid = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Question = models.ForeignKey(QuizQuestions, on_delete=models.CASCADE)
    UserAnswer = models.CharField(max_length=1)  # Assuming user's answer is a single character (A, B, C, or D)
    DateCreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'UserAnswers'
        verbose_name_plural = "UserAnswers"

class UserScores(models.Model):
    Scoreid = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Quiz = models.ForeignKey(QuizQuestions, on_delete=models.CASCADE)
    Score = models.IntegerField()
    DateCreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'UserScores'
        verbose_name_plural = "UserScores"

# test


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for the CustomUser model.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create a new user with the given email and full name.

        Args:
            email (str): The user's email address.
            password (str): The user's password.
            extra_fields: Additional fields to save in the user model.

        Returns:
            CustomUser: The created user instance.

        Raises:
            ValueError: If email is not provided.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create a new superuser with the given email and full name.

        Args:
            email (str): The superuser's email address.
            password (str): The superuser's password.
            extra_fields: Additional fields to save in the superuser model.

        Returns:
            CustomUser: The created superuser instance.

        Raises:
            ValueError: If is_staff or is_superuser is not set to True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    """
    Custom user model with fields for full name, email, password, confirm_password,
    phone number, is_staff, and is_superuser.
    """

    first_name = models.CharField(max_length=150)
    age = models.CharField(max_length=150)
    gender = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    confirm_password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'age', 'gender']

    def get_by_natural_key(self, email_):
        """
        Retrieve a user's unique identifier by their email.

        Args:
            email_: The user's email address.

        Returns:
            The user instance associated with the provided email.
        """
        return self.get(email=email_)

    def __str__(self):
        """
        Return a string representation of the user.

        Returns:
            The user's email as a string.
        """
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Check if the user has the specified permission.

        Args:
            perm: The permission to check.
            obj: The object on which the permission is checked (default is None).

        Returns:
            True if the user has the specified permission, otherwise False.
        """
        return self.is_staff

    def has_module_perms(self, app_label):
        """
        Check if the user has permissions to view the specified app.

        Args:
            app_label: The label of the app for which permissions are checked.

        Returns:
            True if the user has permissions for the app, otherwise False.
        """
        return self.is_staff

    
class kuizDocUser(CustomUser):
    """
    Subclass of CustomUser for non-litigant users.
    """
    pass
