from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}
    return render(request, "index.html", context)

def login(request):
    context = {}
    return render(request, "registration/login.html", context)

def signup(request):
    context = {}
    return render(request, "registration/signup.html", context)
