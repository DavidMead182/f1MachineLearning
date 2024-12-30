from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

import fastf1
from datetime import datetime

# Create your views here.
def index(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        if year:
            context = get_schedule(int(year))
            return render(request, 'index.html', context)
        
    context = get_schedule()
    return render(request, 'index.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or password is incorrect')            
    context = {}
    return render(request,'registration/login.html',context)

def signup(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created successfully ' + user)
            return redirect('login')
        
    context = {'form': form}
    # messages.info(request, 'Username or password is incorrect')
    return render(request, 'registration/signup.html', context)
    
def logouts(request):
    logout(request)
    return redirect('index')

def about_page(request):
    return render(request, 'about.html')

def nextSteps(request):
    return render(request, 'nextSteps.html')

from django.views.generic import ListView, DetailView
from .models import Dashboard

def dashboards(request):
    context = {'object_list': Dashboard.objects.all()}

    return render(request, 'dashboard_list.html', context)

def dashboard(request, pk):
    content = Dashboard.objects.get(pk=pk).get_content()

    print(type(content))
    context = {'object': Dashboard.objects.get(pk=pk),
               'content': content}
    return render(request, 'dashboard_detail.html', context)





def get_schedule(current_year=datetime.now().year):
    
    errors = None
    if current_year < 1950:
        current_year = datetime.now().year
        errors = f"No data for this year, defaulting to current year"
    elif current_year > datetime.now().year:
        current_year = datetime.now().year
        errors = f"No data for this year, defaulting to current year"
    
    schedule_list = []
    schedule = fastf1.get_event_schedule(year=current_year, include_testing=False)

    for i in range(len(schedule)):
        temp_event = schedule.get_event_by_round(i+1)
        event_format = "Conventional" if temp_event.get("EventFormat", "-") == "conventional" else "Sprint Qualification"
        temp_dict = {
            "round": temp_event.get("RoundNumber", "-"),
            "event_name": temp_event.get("EventName", "-"),
            "weekend": f"{temp_event.get('Session1Date', '-').strftime('%d %b')} - {temp_event.get('Session5Date', '-').strftime('%d %b')}" if temp_event.get('Session1Date') and temp_event.get('Session5Date') else "-",
            "location": temp_event.get("Location", "-"),
            "country": temp_event.get("Country", "-"),
            "type": event_format,
        }
        schedule_list.append(temp_dict)

    

    context = {
        "year": current_year,
        "schedule": schedule_list,
        "errors": errors,
        "available_years": list(range(1950, datetime.now().year+1)),
        "current_year": current_year
    }
    return context
