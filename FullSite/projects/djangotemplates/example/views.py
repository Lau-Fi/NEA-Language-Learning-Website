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
import numpy as np

@login_required #All login required decorators simply require the user to be logged in for these subroutines to run. This prevents the user from using the website if they are logged out 
def practicehtml(request):
    questions_html = []
    for instance in Question.objects.filter(lang_id = '1'):  # it's not serialization, but extracting of the useful fields. Takes all questions from the database that have the lang_id of 1 which is Japanese.
        questions_html.append({'id': instance.id, 'q': instance.question, 'a': instance.answer})                                                     
    return render(request, 'practicehtml.html', {'Questions': questions_html}) #Requests the page database to be put onto the page. Takes the questions forom the practice_questions table. Returns this data and renders the Japanese practice page

@login_required
def practice_spanish(request): #Does the same as the Japanese practice request but filters by id = 2 which is for Spanish.
    questions_html = []
    for instance in Question.objects.filter(lang_id = '2'):  
        questions_html.append({'id': instance.id, 'q': instance.question, 'a': instance.answer})
    return render(request, 'practicehtml.html', {'Questions': questions_html}) 

@login_required
def quizhtml(request):
    questions_html = [] #Empty questions HTML array
    for instance in random.sample(list(Question.objects.filter(lang_id = 1)), 10): #Takes 10 random sample of question objects from the Question table with the ID of 1 (Japanese)
        questions_html.append({'id': instance.id, 'q': instance.question, 'a': instance.answer}) # Appends the id, question and answers from the database to the empty questions HTML array 
    return render(request, 'quizhtml.html', {'Questions': questions_html, 'Language': 1}) #Renders the quiz html page with the Questions HTML Array that has now been filled and the language = 1  


@login_required
def quiz_spanish(request): #The same as the Japanese quiz request but for Spanish (lang_id = 2)
    questions_html = []
    for instance in random.sample(list(Question.objects.filter(lang_id = 2)), 10):
        questions_html.append({'id': instance.id, 'q': instance.question, 'a': instance.answer})
    return render(request, 'quizhtml.html', {'Questions': questions_html, 'Language': 2}) 

@csrf_exempt #The subroutine is exempt from CSRF (cross site request forgery) validation. This is due to an error when this program is both running from my computer and I am logged in locally.
@login_required 
def quiz_results(request): #For getting and calculating the quiz score this subroutine is run.
    if request.method == 'POST': #The method of request is POST as we are updating the database
        correct_answers = request.POST['correct_answers'] 
        wrong_answers = request.POST['wrong_answers']
        lang = Lang.objects.get(id = request.POST['lang'])
        difficulty = request.POST.get('difficulty', None)
        user = request.user
        try:
            stats = Stats.objects.get(user = request.user, lang = lang, difficulty = difficulty) 
            stats.correct_answers = int(stats.correct_answers) + int(correct_answers) #The correct answers from the stats in the database will have the correct_answers variable from the website added onto it.
            stats.wrong_answers = int(stats.wrong_answers) + int(wrong_answers) #This is the same for the wrong answers 
            stats.save()
        except ObjectDoesNotExist: #if the object of Stats does not exist the stats variable will be saved as the Stats table and all its keys 
            stats = Stats( user=user, correct_answers = correct_answers, wrong_answers = wrong_answers, lang = lang, difficulty = difficulty)
            stats.save() #This will be then saved 
        return redirect ('scores') 
         



@login_required
def chat(request): #Requests and returns the html page
    return render(request, "chat.html")

@login_required
def room(request, room_name): #Requests asnd returns the chatroom page. However, the URL defined can be changed easily. In our case the chatrooms appened onto the URL is the Japanese or Spanish room. 
    return render(request, "chatrooms/room.html", {"room_name": room_name}) #They both share the same render request through using the colon identity key

@login_required
def home(request):
    users = []
    leaderboard_scores = {}
    for position in Stats.objects.all():
        user_id = position.user
        correct_answers = position.correct_answers
        if user_id in leaderboard_scores:
            leaderboard_scores[user_id] = int(correct_answers) + int(leaderboard_scores[user_id])
        else:
            leaderboard_scores[user_id] = int(correct_answers)
    for user in sorted(leaderboard_scores, key=leaderboard_scores.get, reverse=True):
        users.append([user, ':', leaderboard_scores[user]])    
    return render(request, 'index.html', {'homeboard': users[:10]})

def registration(request):
    return render (request, "registration.html" ) 

@login_required
def profile(request):
    profile = Profile.objects.get(user = request.user) #When returning the profile request we get all the objects from the database Profile table. 
    return render (request, "profile.html", {"userinfo": {'bio': profile.bio, 'picture': profile.picture}}) #When rendering the profile html page we use a JSON dictionary to set the profile keys to variables to use within the Django code.  

def register(request): #When the registering page is loaded we need to run this subroutine to update the database with the user's information
    if request.method == 'POST': #Due to updating/adding new information we use a POST request method
        first_name = request.POST['first_name'] #All of these are stored as variables to use while registering and to store for logging in.
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        bio = request.POST['bio']
        picture = request.POST['picture']
        
        if password==confirm_password: #For verification that the user has to enter their password twice in password and confirm_password
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken') #If the username already exists the user will be notified taht it is already taken. This is to prevent login errors.
                return redirect(register)
            elif User.objects.filter(email=email).exists(): #The same exisits for the email
                messages.info(request, 'Email is already taken')
                return redirect(register) #The user will remain on the register page (get redirected back to it) so they can keep on logging in without any errors
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name) #The .create_user in built django class will be used to create the user. For the fields will be saved into variables.
                user.save() #The whole user account is saved.
                
                profile = Profile(bio=bio, picture=picture, user=user) #For parts of the profile the profile is also defined and saved.
                profile.save()
                
                return redirect('login_user') #Once registewred the user will instantly be redirected to login to the webite


        else:
            messages.info(request, 'Both passwords are not matching') #If the verification fails the user will be told that both their passwords are not matching
            return redirect(register) #They will then stay on the register page
            

    else:
        return render(request, 'registration.html') #Anything else that happens will keep the user on the registration page to avoid errors. 

@login_required
def scores(request):
     try:
        correct_answers = 0
        wrong_answers = 0
        for stat in Stats.objects.filter(user = request.user):
            correct_answers += int(stat.correct_answers)
            wrong_answers += int(stat.wrong_answers)
        return render (request, "scores.html", {"homeinfo": {'correct_answers': correct_answers, 'wrong_answers': wrong_answers}})
     except Stats.DoesNotExist:
        return render (request, 'scores.html')

def login_user(request): #The user login subroutine is run for when the user logs in
    if request.method == 'POST': #We just need the username and password from the database. Why do we need a post if we are not updating information???
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password = password) #The auth.authenticate is built in with django to authenticate whether what the user has entered matches with the registered information. It will check the stored database 

        if user is not None: #The authenticate will return something that is not None so this if statement will run if the user is authenticated and what they entered is valid.
            auth.login(request, user) #An authenticated login bringing the request and the whole user profile 
            return redirect('/index') #Will be returned and redirected with this authenticated profile into the home page (index). 
        else:
            messages.info(request, 'Invalid Username or Password') #If the user fails the else selection will trigger displaying to the user that either their username or password is invalid.
            return redirect('login_user') #Will keep them on the login user page
    
    else:
        return render(request, 'login.html') #Anything else that occurs will render the login html page again

@login_required
def update_user(request): #For updating the user on their profile we use a post request method.
    if request.method == 'POST':
        userprofile = Profile.objects.get(user = request.user) #These will be POST.get however due to all of these already existing in the database having been selected when registering.
        user = request.user
        first_name = request.POST.get('first_name',None)
        last_name = request.POST.get('last_name',None) 
        username = request.POST.get('username',None)
        email = request.POST.get('email',None) 
        password = request.POST.get('password',None)
        confirm_password = request.POST.get('confirm_password',None) 
        bio = request.POST.get('bio',None) 
        picture = request.POST.get('picture',None)
        
        #When the data is loaded into the update form the user can edit the fields and enter new data. Any blank spaces are not allowed using the .strip() inbuilt function. If there is none in the field a message will be displayed asking the user to put valid text in their profile update
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
        if password is not None or confirm_password is not None: #The passwords both are seperate fields for their update but are still set and saved as just password
            if password and confirm_password and password.strip() and confirm_password.strip():
                if password==confirm_password:
                    user.set_password(password) 
                else:
                    messages.info(request, 'Passwords do not match')
                    return redirect(update_user)

        #Saves both user and userprofile at the end of the subroutine
        user.save()
        userprofile.save()
        auth.login(request, user)
        return redirect(profile) #Keeps them on the profile page where they can update their profile
    else:
        return render(request, 'profile.html') 
       

def logout_user(request): #Logging out the user uses the auth.logout function and returns the user back to the sign in page of login_user
    auth.logout(request)
    return redirect('login_user')

# Here we add the class views for some static pages with little django python code on them.
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