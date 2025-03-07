from django.test import TestCase
from .models import Quiz, Question, Answer

class QuizTestCase(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(title="Тестова вікторина", description="Опис тесту")
        self.question = Question.objects.create(quiz=self.quiz, text="Як тебе звати?")
        self.answer = Answer.objects.create(question=self.question, text="Джон", is_correct=True)

    def test_quiz_creation(self):
        self.assertEqual(self.quiz.title, "Тестова вікторина")

    def test_question_creation(self):
        self.assertEqual(self.question.text, "Як тебе звати?")

    def test_answer_creation(self):
        self.assertEqual(self.answer.text, "Джон")
        self.assertTrue(self.answer.is_correct)
