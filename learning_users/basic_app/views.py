from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileFormInfo

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    # Assume user is not registered
    registered = False

    # Check if form submit method is post
    if request.method == "POST":
        # get form data
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileFormInfo(data=request.POST)

        # check if forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # grab details from base user form and save to db
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # grab details from profile form
            profile = profile_form.save(commit=False)
            profile.user = user

            # check if these is a picture in media files
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            # save it to db if it exists
            profile.save()

            # set registered to true so that it passes the form to template
            registered = True
        else:
            # print errors if there are problems
            print(user_form.errors, profile_form.errors)

    else:
        # if form not posted, create form variables
        user_form = UserForm()
        profile_form = UserProfileFormInfo()
    # render register template to allow user to register
    return render(request, 'basic_app/register.html',
                            {'user_form':user_form,
                            'profile_form':profile_form,
                            'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request, 'basic_app/login.html', {})
