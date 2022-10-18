# djangotemplates/example/urls.py

from django.urls import re_path, path
from example import views



urlpatterns = [
    re_path(r'^$', views.HomePageView.as_view(), name= 'home'), # Notice the URL has been named
    re_path(r'^about/$', views.AboutPageView.as_view(), name= 'about'),
    re_path(r'^chat/$', views.chat, name = 'chat'),
    re_path(r'^play/$', views.PlayPageView.as_view(), name = 'play'),
    re_path(r'^profile/$', views.ProfilePageView.as_view(), name = 'profile'),
    re_path(r'^scores/$', views.ScoresPageView.as_view(), name = 'scores'),
    re_path(r'^settings/$', views.SettingsPageView.as_view(), name = 'settings'),
    re_path(r'^practice_languages/$', views.Practice_languagesPageView.as_view(), name = 'practicelang'),
    re_path(r'^practicehtml/$', views.practicehtml, name = 'practicehtml'),
    re_path(r'^quiz_languages/$', views.Quiz_languages.as_view(), name = 'quiz_languages'),
    re_path(r'^quizhtml/$', views.quizhtml, name = 'quizhtml'),
    path("chatrooms/<str:room_name>/", views.room, name="room"),

]

# google regex 
# google JSON 

# https://github.com/CalebCurry/python/tree/master/python/webdev 






