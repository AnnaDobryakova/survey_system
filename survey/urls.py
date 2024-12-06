from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_survey, name='create_survey'),
    path('create/<int:survey_id>/question/', views.create_question, name='create_question'),
    path('create/question/<int:question_id>/choice/', views.create_choice, name='create_choice'),
    path('take/<int:survey_id>/', views.take_survey, name='take_survey'),
    path('results/<int:survey_id>/', views.survey_results, name='survey_results'),
    path('comment/<int:survey_id>/', views.add_comment, name='add_comment'),
    path('surveys/create/question/<int:question_id>/choice/', views.create_choice, name='create_choice'),
    path('surveys/create/finish/<int:survey_id>/', views.finish_survey_creation, name='finish_survey_creation'),
    path('surveys/create/', views.create_survey, name='create_survey'),
    path('surveys/take/<int:survey_id>/', views.take_survey, name='take_survey'),
    path('surveys/results/<int:survey_id>/', views.survey_results, name='survey_results'),
]