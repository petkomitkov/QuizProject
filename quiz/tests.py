from django.test import TestCase
from quiz.models import Category, Question, Quiz


class CategoryMethodTests(TestCase):

    def test_str_method(self):
        category_name = "CS"
        category = Category(category_name=category_name)
        self.assertEqual(str(category), 'CS')

    def test_get_highest_score(self):
        category_name = 'CS'
        highest_score = 125
        category = Category(category_name= category_name,
                            highest_score=highest_score)
        self.assertEqual(category.get_highest_score(), highest_score)


class QuestionMethodTests(TestCase):

    def test_str_method(self):
        question_text = "Some text"
        question = Question(question_text=question_text)
        self.assertEqual(str(question), "Some text")

    def test_get_answers_list_with_no_answers(self):

        question_text = "Some text"
        question = Question(question_text=question_text)
        self.assertEqual(question.get_answers_list(), [])

class QuizMethodTests(TestCase):

    def test_str_method(self):
        quiz = Quiz(name = 'quiz')
        self.assertEqual(str(quiz), 'quiz')









