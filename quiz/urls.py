from django.conf.urls import url
from . import views

app_name = 'quiz'
urlpatterns = [
	url(r'^$', views.front_page, name = 'front_page'),
	url(r'^home/$', views.home, name = 'home'),
	url(r'^scoreboard/$', views.scoreboard, name = 'scoreboard'),
	url(r'^categories/$', views.categories, name = 'categories'),
	url(r'^about/$', views.about, name = 'about'),
	url(r'^logout/$',views.logout_user, name = 'logout'),
	url(r'^quiz/(?P<category_name>\w+)/$',views.start_quiz, name =  'start_quiz'),
	url(r'^next/$', views.next, name = 'next'),
	url(r'^results/(?P<category>\w+)/$', views.results, name = 'results')
]
