from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.quiz_list, name='quiz_list'),
    path('create/', views.quiz_create, name='quiz_create'),
    path('question/create/', views.question_create, name='question_create'),
    path('answer/create/', views.answer_create, name='answer_create'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/add_question/', views.add_question, name='add_question'),
    path('results/', views.results, name='results'),
    #path('quiz/<int:quiz_id>/play_quiz/', views.play_quiz, name='play_quiz'),
    path('quiz/<int:quiz_id>/play/<int:question_number>/', views.play_quiz, name='play_quiz'),
    path('quiz/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
    path('quiz/', views.quiz_list, name='quiz_list'),
    

]





