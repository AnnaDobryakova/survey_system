from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Survey, Question, Choice, Answer, Comment
from .forms import SurveyForm, QuestionForm, ChoiceForm, AnswerForm, CommentForm

@login_required
def home(request):
    surveys = Survey.objects.all()
    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'surveys/home.html', {'surveys': surveys, 'comments': comments})

@login_required
def create_survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.creator = request.user
            survey.save()
            return redirect('edit_survey', survey_id=survey.id)
    else:
        form = SurveyForm()
    return render(request, 'surveys/create_survey.html', {'form': form})

@login_required
def edit_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    if request.method == 'POST':
        form = SurveyForm(request.POST, instance=survey)
        if form.is_valid():
            form.save()
            return redirect('edit_survey', survey_id=survey.id)
    else:
        form = SurveyForm(instance=survey)
    return render(request, 'surveys/edit_survey.html', {'form': form, 'survey': survey})

@login_required
def add_question(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()
            return redirect('edit_survey', survey_id=survey.id)
    else:
        form = QuestionForm()
    return render(request, 'surveys/add_question.html', {'form': form, 'survey': survey})

@login_required
def add_choice(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.save()
            return redirect('edit_survey', survey_id=question.survey.id)
    else:
        form = ChoiceForm()
    return render(request, 'surveys/add_choice.html', {'form': form, 'question': question})

@login_required
def take_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    if request.method == 'POST':
        for question in survey.question_set.all():
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id:
                choice = get_object_or_404(Choice, id=choice_id)
                Answer.objects.create(question=question, choice=choice, user=request.user, survey=survey)
        return redirect('survey_results', survey_id=survey.id)
    else:
        forms = {}
        for question in survey.question_set.all():
            forms[question.id] = AnswerForm(prefix=str(question.id))
    return render(request, 'surveys/take_survey.html', {'survey': survey, 'forms': forms})

@login_required
def survey_results(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    results = Answer.get_results(survey)
    return render(request, 'surveys/survey_results.html', {'survey': survey, 'results': results})

@login_required
def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'surveys/add_comment.html', {'form': form})

@login_required
def clear_lists(request):
    if request.method == 'POST':
        Survey.objects.all().delete()
        Comment.objects.all().delete()
        return redirect('home')
    return redirect('home')