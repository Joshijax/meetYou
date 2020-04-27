from django.shortcuts import render
from django.shortcuts import render

from django.conf import settings
from django.contrib import messages 
from django.http import HttpResponse
from .forms import LoginUpForm, SignUpForm
from functools import wraps
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.db.models import Q
from chat.models import Online
def wrappers(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped

def is_logged_in(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated == True:
            return redirect('home')
        else:

            return f(request, *args, *kwargs)

    return wrap

# Create your views here.
@is_logged_in
def index(request):
    if request.method == 'POST':
        form = LoginUpForm(data=request.POST)
        
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            
            login(request, user)
            
            request.session['username'] = username
            messages.info(request, f"you are logged in as {username} ")
            return redirect('home')
            
        
    else:
        form = LoginUpForm()
      
    return render(request, 'Login.html',  {'form': form,})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=raw_password)
            
            
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
@login_required(login_url='/')
def home(request):
    users = User.objects.all()
    return render(request, 'home.html', {'users': users,})


def logout_request(request):

    logout(request)
    
    return redirect('/')

