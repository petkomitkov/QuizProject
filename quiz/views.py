from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import Category, Question, Choice, Score
from random import shuffle

def front_page(request):
	if request.POST.get("mybtn"):
		user = authenticate(username = request.POST['username'],password = request.POST['password'])
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect(reverse('quiz:home'))
			else:
				return render(request,'quiz/front_page.html', {'error_message':"You're account is currently inactive and you cannot login with it!"})
		else:
			return render(request,'quiz/front_page.html', {'error_message':"The login information is incorrect!"})
	else:
		return render(request, 'quiz/front_page.html')

@login_required
def home(request):
	title = 'Quizle'
	return render(request,'quiz/home.html', {'title': title})

@login_required	
def scoreboard(request):
	scoreboard = list(Score.objects.all())
	scoreboar_sorted = sorted(scoreboard, key = lambda x: x.score, reverse = True)[:10]
	context = {'scoreboard': scoreboar_sorted, 'title': 'Quizle' }
	return render(request, 'quiz/scoreboard.html', context)

@login_required
def about(request):
	return render(request, 'quiz/about.html', {'title':'Quizle'})

@login_required
def categories(request):
	context = {
		'title': 'Quizle',
		'categories': Category.objects.all(),
	}

	return render(request, 'quiz/categories.html', context)

def logout_user(request):
	logout(request)
	return redirect(reverse('quiz:front_page'))

def start_quiz(request, category_name):
	question_list = list(Question.objects.filter(category__category_name = category_name))
	question_list_pk = list(map(lambda x: x.id, question_list))
	shuffle(question_list_pk)
	request.session['is_active'] = True
	request.session['question_list_pk'] = question_list_pk
	request.session['current_question'] = 0
	request.session['score'] = 0
	request.session['last_question'] = len(question_list_pk) - 1
	context = {
		'question': Question.objects.get(id = request.session['question_list_pk'][request.session['current_question']]),
		'title': 'Quizle',
	}
	return render(request, 'quiz/question.html', context)

def next(request):
	question = Question.objects.get(id = request.session['question_list_pk'][request.session['current_question']])

	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'quiz/question.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		if request.session['current_question'] == request.session['last_question']:
			if selected_choice.choice_is_correct: 
				request.session['score'] += question.question_points
			return HttpResponseRedirect(reverse('quiz:results', kwargs={'category': str(question.category.category_name) }))
		else:	
			request.session['current_question'] += 1
			if selected_choice.choice_is_correct: 
				request.session['score'] += question.question_points
			question = Question.objects.get(id = request.session['question_list_pk'][request.session['current_question']])
			context = {
				'question': question,
				'title': 'Quizle',
			}
			return render(request, 'quiz/question.html', context)

def results(request, category):
	if request.session['is_active'] == False:
		return HttpResponseRedirect(reverse('quiz:home'))
	context = {
		'score': request.session['score'],
		'title':'	Quizle'
	}
	username = request.user.username
	score = Score(name = username, category_name = category, score = request.session['score'])
	score.save()
	return render(request,'quiz/results.html', context)


	