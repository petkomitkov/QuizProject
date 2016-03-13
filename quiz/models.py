from django.db import models
from django.core.exceptions import ImproperlyConfigured


class Category(models.Model):
    category_name = models.CharField(max_length=10)
    highest_score = models.IntegerField(default=0)

    def __str__(self):
        return self.category_name


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    question_points = models.IntegerField(default=5)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

    def get_answers_list(self):
        return [(answer.id, answer.choice_text) for answer in
                self.choice_set.all()]


class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    choice_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ['choice_is_correct']

    def __str__(self):
        return self.choice_text


class ScoreManager(models.Manager):
    def new_score(self, **kwargs):
        name = kwargs['name']
        category_name = kwargs['category_name']
        score = kwargs['score']
        new_score = self.create(name = name,
                                category_name = category_name,
                                score = score)
        return new_score


class Score(models.Model):
    name = models.CharField(max_length=40)
    category_name = models.CharField(max_length=40)
    score = models.IntegerField(default=0)
    objects = ScoreManager()

    def __str__(self):
        return self.name + ' ' + self.category_name + ' ' + str(self.score)


class QuizManager(models.Manager):

    def new_quiz(self, category):

        try:
            new_quiz = list(Quiz.objects.all())[0]
        except IndexError:

            question_set = Question.objects.filter(category__category_name=category)

            if len(question_set) == 0:
                raise ImproperlyConfigured("There are no questions in this category!")

            question_set = question_set.values_list('id', flat=True)
            questions = ",".join(map(str, question_set)) + ","
            new_quiz =  self.create(name = category,
                                    question_list = questions,
                                    current_score = 0,
                                    complete = False)

        return new_quiz


class Quiz(models.Model):
    name = models.CharField(max_length=40)

    question_list = models.CommaSeparatedIntegerField(max_length=512)

    current_score = models.IntegerField(default=0)

    complete = models.BooleanField(default=False)

    objects = QuizManager()

    def get_question(self):
        if not self.question_list:
            return False
        first, _ = self.question_list.split(',', 1)
        question_id = int(first)
        return Question.objects.get(id = question_id)

    def remove_first_question(self):
        if not self.question_list:
            return

        _, other_questions = self.question_list.split(',', 1)
        self.question_list = other_questions
        self.save()

    def add_to_score(self, points):
        self.current_score += int(points)
        self.save()

    def __str__(self):
        return self.name
