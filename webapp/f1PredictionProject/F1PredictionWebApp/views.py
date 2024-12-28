from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout

import fastf1 as ff1

# Create your views here.
def index(request):
    context = {"season":2024}
    # last_race_id, year, schedule = most_recent_race()
    # session = ff1.get_session(year, last_race_id, 'R')
    # session.load()
    # df = pd.DataFrame(session.results)
    # df['Position'] = df['Position'].astype(int)
    # results = df[['Position', 'Abbreviation']]

    # # path = telementry(year, last_race_id)

    # context = { "eventName": session.event['EventName'],
    #     "results": results.to_dict(orient='records')}
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

class DashboardListView(ListView):
    model = Dashboard
    template_name = 'dashboard_list.html'

class DashboardDetailView(DetailView):
    model = Dashboard
    template_name = 'dashboard_detail.html'








# Helper functions
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colormaps
from matplotlib.collections import LineCollection
import fastf1
from datetime import date,datetime, timezone,timedelta
import fastf1
import pandas as pd
import os

def most_recent_race():
    today = date.today()
    year = today.year
    schedule = fastf1.get_event_schedule(year)
    utc_now = datetime.now(timezone.utc) + timedelta(hours=4)
    last_race_id = 0
    for dates in schedule['Session5Date']:
        if pd.isna(dates):
            continue
        else:
            if dates < utc_now:
                last_race_id = last_race_id +1
    print(schedule.loc[last_race_id, "EventName"])
    return last_race_id, year, schedule

def telementry(year, session_number):
    schedule = fastf1.get_event_schedule(year)
    session = fastf1.get_session(year, session_number, 'R')
    session.load()
    
    lap = session.laps.pick_fastest()
    tel = lap.get_telemetry()

    x = np.array(tel['X'].values)
    y = np.array(tel['Y'].values)
    
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    gear = tel['nGear'].to_numpy().astype(float)

    cmap = colormaps['Paired']
    lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
    lc_comp.set_array(gear)
    lc_comp.set_linewidth(4)

    plt.gca().add_collection(lc_comp)
    plt.axis('equal')
    plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)
    
    title = plt.suptitle(
        f"Fastest Lap Gear Shift Visualization\n"
        f"{lap['Driver']} - {session.event['EventName']} {session.event.year}"
    )
    
    cbar = plt.colorbar(mappable=lc_comp, label="Gear",
                        boundaries=np.arange(1, 10))
    cbar.set_ticks(np.arange(1.5, 9.5))
    cbar.set_ticklabels(np.arange(1, 9))

    if os.path.exists('./F1PredictionWebApp/static/images/recent_tel.png'):
            os.remove('./F1PredictionWebApp/static/images/recent_tel.png')  # Remove the existing file
    
    plt.savefig('./F1PredictionWebApp/static/images/recent_tel.png', bbox_inches='tight', dpi=300)

    return '/images/recent_tel.png'
