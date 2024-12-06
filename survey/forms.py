from django import forms
from .models import Survey, Question, Choice, Answer, Comment


class SurveyForm (forms.ModelForm):

    start_date = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )
    end_date = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )

    class Meta:
        model = Survey
        fields = ['title', 'description', 'start_date', 'end_date', 'max_participants', 'password_protected', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password_protected = cleaned_data.get('password_protected')
        password = cleaned_data.get('password')
        if password_protected and not password:
            self.add_error('password', 'Password is required for password-protected surveys.')
        return cleaned_data


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type']


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['choice', 'text_answer']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']