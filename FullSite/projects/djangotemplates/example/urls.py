# djangotemplates/example/urls.py

from django.urls import re_path
from example import views

urlpatterns = [
    re_path(r'^$', views.HomePageView.as_view(), name='home'), # Notice the URL has been named
    re_path(r'^about/$', views.AboutPageView.as_view(), name='about'),
    re_path(r'^chat/$', views.ChatPageView.as_view(), name =  'chat'),
    re_path(r'^play/$', views.PlayPageView.as_view(), name =  'play'),
    re_path(r'^profile/$', views.ProfilePageView.as_view(), name =  'profile'),
    re_path(r'^scores/$', views.ScoresPageView.as_view(), name =  'scores'),
    re_path(r'^settings/$', views.SettingsPageView.as_view(), name =  'settings'),
    re_path(r'^practice_languages/$', views.Practice_languagesPageView.as_view(), name =  'practicelang'),
    re_path(r'^practicehtml/$', views.Practicehtml.as_view(), name =  'practicehtml'),

]



# https://github.com/CalebCurry/python/tree/master/python/webdev 