# djangotemplates/example/views.py
from django.shortcuts import render
from django.views.generic import TemplateView # Import TemplateView
from .models import Question 

def practicehtml(request):
    question = Question.objects.all()
    return render(request, 'practicehtml.html', {'Question': question}) #Requests the page database to be put onto the page? Takes the questions forom the practice_questions table


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



                                                                                 