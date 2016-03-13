from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, TemplateView, RedirectView, FormView
from .models import Category, Choice, Score, Quiz
from django.utils.decorators import method_decorator
from .forms import QuestionForm


class FrontPage(View):
    def get(self, request):
        return render(request, 'quiz/front_page.html')

    def post(self, request):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('quiz:home'))
            else:
                return render(request,
                              'quiz/front_page.html',
                              {'error_message': "You're account is currently inactive and you cannot login with it!"})
        else:
            return render(request,
                          'quiz/front_page.html',
                          {'error_message': "The login information is incorrect!"})

@method_decorator(login_required, name = 'dispatch')
class Home(TemplateView):
    template_name = 'quiz/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data()
        context['title'] = 'Quizle'
        return context

@method_decorator(login_required, name='dispatch')
class Scoreboard(ListView):
    template_name = 'quiz/scoreboard.html'
    context_object_name =  'scoreboard'

    def get_queryset(self):
        return Score.objects.order_by('-score')[:10]

    def get_context_data(self, **kwargs):
        context = super(Scoreboard, self).get_context_data()
        context['title'] = 'Quizle'
        return context

@method_decorator(login_required, name = 'dispatch')
class About(TemplateView):
    template_name = 'quiz/about.html'

    def get_context_data(self, **kwargs):
        context = super(About, self).get_context_data()
        context['title'] = 'Quizle'
        return context

@method_decorator(login_required, name = 'dispatch')
class Categories(ListView):
    template_name = 'quiz/categories.html'
    model = Category
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super(Categories, self).get_context_data()
        context['title'] = 'Quizle'
        return context

class LogoutView(RedirectView):
    url = reverse_lazy('quiz:front_page')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

class AnswerQuiz(FormView):
    form_class = QuestionForm
    template_name = 'quiz/question.html'

    def dispatch(self, request, *args, **kwargs):
        self.quiz = Quiz.objects.new_quiz(category = self.kwargs['category_name'])
        return super(AnswerQuiz, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class):
        self.question = self.quiz.get_question()
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(AnswerQuiz, self).get_form_kwargs()

        return dict(kwargs, question=self.question)

    def form_valid(self, form):
        answer = form.cleaned_data['answers']
        is_correct = Choice.objects.get(pk = answer).choice_is_correct
        if is_correct:
            self.quiz.add_to_score(self.question.question_points)

        self.quiz.remove_first_question()

        if self.quiz.get_question() is False:
            return self.result()

        self.request.POST = {}

        return super(AnswerQuiz, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(AnswerQuiz, self).get_context_data()
        context['question'] = self.question
        context['quiz'] = self.quiz
        context['title'] = 'Quizle'
        return context

    def result(self):
        results = {
            'quiz': self.quiz,
            'score': self.quiz.current_score,
            'title': 'Quizle'
        }

        score = Score.objects.new_score(name = self.request.user.username,
                                        category_name=self.quiz.name,
                                        score = self.quiz.current_score)

        score.save()
        self.quiz.delete()
        return render(self.request, 'quiz/results.html', results)


