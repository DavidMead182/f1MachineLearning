from django.shortcuts import render
from .helper_functions import *
import fastf1 as ff1

# Create your views here.
def index(request):
    context = {}
    last_race_id, year, schedule = most_recent_race()
    session = ff1.get_session(year, last_race_id, 'R')
    session.load()
    df = pd.DataFrame(session.results)
    results = df[['Position', 'Abbreviation']]
    context = {"results": results.to_dict(orient='records')}
    return render(request, 'index.html', context)

def login(request):
    context = {}
    return render(request, "registration/login.html", context)

def signup(request):
    context = {}
    return render(request, "registration/signup.html", context)
