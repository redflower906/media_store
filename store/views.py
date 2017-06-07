from django.shortcuts import render
#from django.http import HttpResponse

def index(request):
    return render (request, "store/base.html")

def get_services(request):
	result_set = []
	

