from django.db import models

class Category(models.Model):
	category_name = models.CharField(max_length = 10)
	highest_score = models.IntegerField(default = 0)

	def __str__(self):
		return self.category_name
		
class Question(models.Model):
	question_text = models.CharField(max_length = 200)
	question_points = models.IntegerField(default = 5)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)

	def __str__(self):
		return self.question_text

class Choice(models.Model):
	choice_text = models.CharField(max_length = 200)
	choice_question = models.ForeignKey(Question, on_delete = models.CASCADE)
	choice_is_correct = models.BooleanField(default = False)



class Score(models.Model):
	name = models.CharField(max_length = 40)
	category_name = models.CharField(max_length = 40)
	score = models.IntegerField(default = 0)

	def __str__(self):
		return self.name + ' ' + self.category_name + ' ' +str(self.score)

