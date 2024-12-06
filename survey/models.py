from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_participants = models.IntegerField(default=0)
    password_protected = models.BooleanField(default=False)
    password = models.CharField(max_length=128, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        if self.password_protected and not self.password:
            raise ValueError('Password is required for password-protected surveys.')
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.SET_NULL, null=True, blank=True)

class Question(models.Model):
    TEXT = 'text'
    SINGLE_CHOICE = 'single_choice'
    MULTIPLE_CHOICE = 'multiple_choice'
    NUMBER = 'number'
    FREE_TEXT = 'free_text'

    QUESTION_TYPES = [
        (TEXT, 'Text'),
        (SINGLE_CHOICE, 'Single Choice'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (NUMBER, 'Number'),
        (FREE_TEXT, 'Free Text'),
    ]

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=30, choices=QUESTION_TYPES)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, blank=True, null=True)
    text_answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Answer by {self.user.username} to {self.question.text}'


class Comment(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.survey.title}'
