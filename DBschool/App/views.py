from django.shortcuts import render
# Create your views here.
def join(request):
    return render(request,"App/join.html")

def base(request):
    return render(request,"App/base.html")
