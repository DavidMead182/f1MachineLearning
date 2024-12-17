from django.shortcuts import HttpResponse, render

# Create your views here.
def index(request):
    context = {}
    return render(request, "index.html", context)
