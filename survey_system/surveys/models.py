from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()  
    expires_at = models.DateTimeField(null=True, blank=True)  
    password = models.CharField(max_length=255, null=True, blank=True)  
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=50, choices=[
        ('single_choice', 'Единственный выбор'),
        ('multiple_choice', 'Множественный выбор'),
        ('text', 'Текст'),
        ('number', 'Число'),
        ('date', 'Дата/время'),
    ])

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    survey = models.ForeignKey(Survey, related_name='answers', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.user.username} - {self.question.text} - {self.choice.text}"

    @staticmethod
    def get_results(survey):
        results = {}
        for question in survey.question_set.all():
            choices = Choice.objects.filter(question=question)
            choice_results = {}
            for choice in choices:
                count = Answer.objects.filter(question=question, choice=choice).count()
                choice_results[choice.text] = count
            results[question.text] = choice_results
        return results

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:50]}"