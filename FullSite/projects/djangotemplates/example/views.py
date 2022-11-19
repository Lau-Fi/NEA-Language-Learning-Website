# djangotemplates/example/views.py
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView # Import TemplateView
from .models import Question
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
import random 

@login_required
def practicehtml(request):
    questions_html = []
    for instance in Question.objects.all():  # it's not serialization, but extracting of the useful fields
        questions_html.append({'id': instance.id, 'q': instance.Question, 'a': instance.Answer})
    return render(request, 'practicehtml.html', {'Questions': questions_html}) #Requests the page database to be put onto the page? Takes the questions forom the practice_questions table

@login_required
def practice_spanish(request):
    questions_html = []
    for instance in Question.objects.filter(id__gt = 51):  
        questions_html.append({'id': instance.id, 'q': instance.Question, 'a': instance.Answer})
    return render(request, 'practice_spanish.html', {'Questions': questions_html}) 

@login_required
def quizhtml(request):
    questions_html = []
    for instance in random.sample(list(Question.objects.filter(id__gt = 51)), 10):
        questions_html.append({'id': instance.id, 'q': instance.Question, 'a': instance.Answer})
    return render(request, 'quizhtml.html', {'Questions': questions_html}) 


@login_required
def quiz_spanish(request):
    questions_html = []
    for instance in random.sample(list(Question.objects.all()),10):
        questions_html.append({'id': instance.id, 'q': instance.Question, 'a': instance.Answer})
    return render(request, 'quiz_spanish.html', {'Questions': questions_html}) 

@login_required
def chat(request):
    return render(request, "chat.html")

@login_required
def room(request, room_name):
    return render(request, "chatrooms/room.html", {"room_name": room_name})

@login_required
def home(request):
    return render (request, "index.html" ) 


def registration(request):
    return render (request, "registration.html" ) 


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect(register)
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect(register)
            else:
                user = User.objects.create_user(username=username, password=password, 
                                        email=email, first_name=first_name, last_name=last_name)
                user.save()
                
                return redirect('login_user')


        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect(register)
            

    else:
        return render(request, 'registration.html')




def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('/index')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login_user')
    
    else:
        return render(request, 'login.html')


def logout_user(request):
    auth.logout(request)
    return redirect('login_user')

# Add the two views we have been talking about  all this time :)
class HomePageView(TemplateView):
    template_name = "login.html"

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

class login(TemplateView):
    template_name = "login.html"


                                                                        