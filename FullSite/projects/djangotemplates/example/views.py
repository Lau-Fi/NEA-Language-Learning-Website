# djangotemplates/example/views.py
from django.shortcuts import render
from django.views.generic import TemplateView # Import TemplateView
from .models import Question
import random 

def practicehtml(request):
    questions_html = []
    for instance in Question.objects.all():  # it's not serialization, but extracting of the useful fields
        questions_html.append({'id': instance.id, 'q': instance.Question, 'a': instance.Answer})
    return render(request, 'practicehtml.html', {'Questions': questions_html}) #Requests the page database to be put onto the page? Takes the questions forom the practice_questions table

def quizhtml(request):
    questions_html = []
    for instance in random.sample(list(Question.objects.all()),10):
        questions_html.append({'id': instance.id, 'q': instance.Question, 'a': instance.Answer})
    return render(request, 'quizhtml.html', {'Questions': questions_html}) 



# Add the two views we have been talking about  all this time :)
class HomePageView(TemplateView):
    template_name = "index.html"

class ChatPageView(TemplateView):
    template_name = "chat.html"

class AboutPageView(TemplateView):
    template_name = "about.html"

class PlayPageView(TemplateView):
    template_name = "play.html"

class ProfilePageView(TemplateView):
    template_name = "profile.html"

class ScoresPageView(TemplateView):
    template_name = "scores.html"

class SettingsPageView(TemplateView):
    template_name = "settings.html"

class Practice_languagesPageView(TemplateView):
    template_name = "practice_languages.html"

class Quiz_languages(TemplateView):
    template_name = "quiz_languages.html"

class Quiz_html(TemplateView):
    template_name = "quizhtml.html"



                                                                                 