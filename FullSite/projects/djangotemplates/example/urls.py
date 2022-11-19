# djangotemplates/example/urls.py

from django.urls import re_path, path, include
from example import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



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
    re_path(r'^practice_spanish/$', views.practice_spanish, name = 'practice_spanish'),
    re_path(r'^quiz_spanish/$', views.quiz_spanish, name = 'quiz_spanish'),
    path("chatrooms/<str:room_name>/", views.room, name="room"),
    path('admin/', admin.site.urls),
    re_path(r"^registration/$", views.registration, name = "registration"),
    re_path(r"^registration/register$", views.register, name = "register"),
    path("login_user", views.login_user, name="login_user"),
    path("index", views.home, name="home"),
    path("logout_user", views.logout_user, name="logout_user"),

]

# google regex 
# google JSON 
