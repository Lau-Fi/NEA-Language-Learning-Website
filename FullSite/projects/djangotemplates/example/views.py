# djangotemplates/example/views.py
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView # Import TemplateView
from .models import *
from django.contrib.auth.models import *
from django.contrib.auth.decorators import login_required
import random 
from django.core.exceptions import *
from django.views.decorators.csrf import *

@login_required
def practicehtml(request):
    questions_html = []
    for instance in Question.objects.filter(lang_id = '1'):  # it's not serialization, but extracting of the useful fields
        questions_html.append({'id': instance.id, 'q': instance.question, 'a': instance.answer})                                                     
    return render(request, 'practicehtml.html', {'Questions': questions_html}) #Requests the page database to be put onto the page? Takes the questions forom the practice_questions table

@login_required
def practice_spanish(request):
    questions_html = []
    for instance in Question.objects.filter(lang_id = '2'):  
        questions_html.append({'id': instance.id, 'q': instance.question, 'a': instance.answer})
    return render(request, 'practicehtml.html', {'Questions': questions_html}) 

@login_required
def quizhtml(request):
    questions_html = []
    for instance in random.sample(list(Question.objects.filter(lang_id = 1)), 10):
        questions_html.append({'id': instance.id, 'q': instance.question, 'a': instance.answer})
    return render(request, 'quizhtml.html', {'Questions': questions_html, 'Language': 1}) 


@login_required
def quiz_spanish(request):
    questions_html = []
    for instance in random.sample(list(Question.objects.filter(lang_id = 2)), 10):
        questions_html.append({'id': instance.id, 'q': instance.question, 'a': instance.answer})
    return render(request, 'quizhtml.html', {'Questions': questions_html, 'Language': 2}) 

@csrf_exempt
@login_required
def quiz_results(request):
    if request.method == 'POST': 
        correct_answers = request.POST.get('correct_answers')
        wrong_answers = request.POST.get('wrong_answers', None)
        lang = request.POST.get('lang', None)
        difficulty = request.POST.get('difficulty', None)
        user = request.user
        try:
            stats = Stats.objects.get(user = request.user, lang = lang, difficulty = difficulty)
            stats.correct_answers += correct_answers
            stats.wrong_answers += wrong_answers 
            stats.save()
        except ObjectDoesNotExist:
            stats = Stats( user=user, correct_answers = correct_answers, wrong_answers = wrong_answers, lang = lang, difficulty = difficulty)
            stats.save()
        return redirect ('home') 
         
        


        


@login_required
def chat(request):
    return render(request, "chat.html")

@login_required
def room(request, room_name):
    return render(request, "chatrooms/room.html", {"room_name": room_name})

@login_required
def home(request):
    stats = Stats.objects.all()
    #return render (request, "index.html", {"homeinfo": {'correct_answers': stats.correct_answers, 'wrong_answers': stats.wrong_answers}}) 
    return render (request, "index.html")

def registration(request):
    return render (request, "registration.html" ) 

@login_required
def profile(request):
    profile = Profile.objects.get(user = request.user)
    return render (request, "profile.html", {"userinfo": {'bio': profile.bio, 'picture': profile.picture}}) 

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        bio = request.POST['bio']
        picture = request.POST['picture']
        
        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect(register)
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect(register)
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save()
                
                profile = Profile(bio=bio, picture=picture, user=user)
                profile.save()
                
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

@login_required
def update_user(request):
    if request.method == 'POST':
        userprofile = Profile.objects.get(user = request.user)
        user = request.user
        first_name = request.POST.get('first_name',None)
        last_name = request.POST.get('last_name',None) 
        username = request.POST.get('username',None)
        email = request.POST.get('email',None) 
        password = request.POST.get('password',None)
        confirm_password = request.POST.get('confirm_password',None) 
        bio = request.POST.get('bio',None) 
        picture = request.POST.get('picture',None)
        

        if bio is not None:
            userprofile.bio = bio 
        if picture is not None:
            userprofile.picture = picture
        if first_name is not None:
            if first_name.strip():
                user.first_name = first_name
            else:
                messages.info(request, 'Please enter a First Name')
                return redirect(update_user)
        if last_name is not None:
            if last_name and last_name.strip():
                user.last_name = last_name
            else:
                messages.info(request, 'Please enter a Last Name')
                return redirect(update_user) 
        if username is not None:
            if username and username.strip():
                user.username = username
            else:
                messages.info(request, 'Please enter a Username')
                return redirect(update_user)
        if email is not None:
            if email and email.strip():
                user.email = email
            else:
                messages.info(request, 'Please enter an email')
                return redirect(update_user)
        if password is not None or confirm_password is not None:
            if password and confirm_password and password.strip() and confirm_password.strip():
                if password==confirm_password:
                    user.set_password(password) 
                else:
                    messages.info(request, 'Passwords do not match')
                    return redirect(update_user)


        user.save()
        userprofile.save()
        auth.login(request, user)
        return redirect(profile)
    else:
        return render(request, 'profile.html')
       

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



# Get requests get a payload from the page - does not have a body
# Post requests are for updating infomation - they do have a body