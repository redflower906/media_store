from django.shortcuts import render
#from django.http import HttpResponse

def index(request):
	return render (request, "templates/store/base.html")

# Create your views here.
