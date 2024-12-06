from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Survey, Question, Choice, Answer, Comment
from .forms import SurveyForm, QuestionForm, ChoiceForm, AnswerForm, CommentForm

# Create your views here.

from django.http import HttpResponse

@login_required
def create_survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.created_by = request.user
            survey.save()
            print(f"Redirecting to create_question with survey ID: {survey.id}")
            return redirect('create_question', survey_id=survey.id)
        else:
            print(f"Form errors: {form.errors}")
            return render(request, 'surveys/create_survey.html', {'form': form})
    else:
        form = SurveyForm()
    return render(request, 'surveys/create_survey.html', {'form': form})

@login_required
def create_question(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()
            return redirect('create_choice', question_id=question.id)
    else:
        form = QuestionForm()
    return render(request, 'surveys/create_question.html', {'form': form, 'survey': survey})

@login_required
def create_choice(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    survey = question.survey
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.save()
            return redirect('create_choice', question_id=question.id)
    else:
        form = ChoiceForm()
    return render(request, 'surveys/create_choice.html', {'form': form, 'question': question, 'survey': survey})

@login_required
def finish_survey_creation(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    return redirect('create_survey')

@login_required
def take_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)

    if request.method == 'POST':
        for question in survey.question_set.all():
            form = AnswerForm(request.POST, prefix=str(question.id))
            if form.is_valid():
                answer = form.save(commit=False)
                answer.user = request.user
                answer.question = question
                answer.save()
        return redirect('survey_results', survey_id=survey.id)
    else:
        forms = {}
        for question in survey.question_set.all():
            forms[question.id] = AnswerForm(prefix=str(question.id))
        return render(request, 'surveys/take_survey.html', {'survey': survey, 'forms': forms})

@login_required
def survey_results(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    results = {}
    for question in survey.question_set.all():
        results[question.id] = Answer.objects.filter(question=question).values_list('text_answer', flat=True)
    return render(request, 'surveys/survey_results.html', {'survey': survey, 'results': results})


@login_required
def add_comment(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.survey = survey
            comment.user = request.user
            comment.save()
            return redirect('survey_results', survey_id=survey.id)
    else:
        form = CommentForm()
    return render(request, 'surveys/add_comment.html', {'form': form, 'survey': survey})