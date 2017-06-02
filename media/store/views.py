from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("Media Store")

# Create your views here.
