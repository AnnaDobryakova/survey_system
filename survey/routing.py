from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/survey/<int:survey_id>/', consumers.SurveyComsumer,as_asgi()),
]