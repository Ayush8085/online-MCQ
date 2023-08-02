from django.urls import path

from . import views

urlpatterns = [
    path("", views.homePage, name="home"),
    path("quiz/<str:pk>/", views.quiz, name="quiz"),
    path("quiz/<str:pk>/data", views.quizData, name="quiz-data"),

    path("quiz/result", views.resultPage, name="result"),
    path("create-quiz/", views.createQuiz, name='create-quiz'),
    path("questions/", views.createQuestions, name='questions'),
]
