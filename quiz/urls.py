from django.conf.urls import url
from quiz.views import  FrontPage, Categories, Scoreboard, Home, About, LogoutView, AnswerQuiz
from . import views

app_name = 'quiz'
urlpatterns = [
	url(r'^$', FrontPage.as_view(), name = 'front_page'),
	url(r'^home/$', Home.as_view(), name = 'home'),
	url(r'^scoreboard/$', Scoreboard.as_view(), name = 'scoreboard'),
	url(r'^categories/$', Categories.as_view(), name = 'categories'),
	url(r'^about/$', About.as_view(), name = 'about'),
	url(r'^logout/$',LogoutView.as_view(), name = 'logout'),
	url(r'^quiz/(?P<category_name>\w+)/$',AnswerQuiz.as_view(), name =  'start_quiz'),
	#url(r'^results/(?P<category>\w+)/$', views.results, name = 'results'),
]
