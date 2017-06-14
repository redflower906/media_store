from django.shortcuts import render
from .models import Inventory
#from django.http import HttpResponse

def index(request):
    my_item = Inventory.objects.get(id=1)
    print (my_item.__dict__)

    context = {'cost': my_item.cost}
    return render (request, "store/base.html", context)

def get_services(request):
    result_set = []
    

