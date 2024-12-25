from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_survey/', views.create_survey, name='create_survey'),
    path('edit_survey/<int:survey_id>/', views.edit_survey, name='edit_survey'),
    path('add_question/<int:survey_id>/', views.add_question, name='add_question'),
    path('add_choice/<int:question_id>/', views.add_choice, name='add_choice'),
    path('take_survey/<int:survey_id>/', views.take_survey, name='take_survey'),
    path('survey_results/<int:survey_id>/', views.survey_results, name='survey_results'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('clear_lists/', views.clear_lists, name='clear_lists'),
]