from django.shortcuts import render
from .models import Inventory
#from django.http import HttpResponse

def index(request):
    myItem = Inventory.objects.get(id=1)
    print (myItem.__dict__)
    context = {'cost' : myItem.cost}
    return render (request, "store/base.html", context)

def login(request):
    return render (request, "store/login.html")

def get_services(request):
    result_set = []

