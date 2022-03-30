from django.shortcuts import render
# Create your views here.
def join(request):
    return render(request,"App/join.html")

def home(request):
    return render(request, "App/home.html")
