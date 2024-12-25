from django import forms
from .models import Survey, Question, Choice, Answer, Comment

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description', 'expires_at', 'password']
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'expires_at': 'Дата истечения',
            'password': 'Пароль',
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type']
        labels = {
            'text': 'Текст вопроса',
            'question_type': 'Тип вопроса',
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text']
        labels = {
            'text': 'Текст варианта',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['choice']  
        labels = {
            'choice': 'Выбранный вариант',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Текст комментария',
        }