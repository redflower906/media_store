from django.shortcuts import render
from django.template import context
## from nameform 
from .forms import NameForm
from django.http import HttpResponseRedirect
from .models import Inventory
#from django.http import HttpResponse

def currentURL(request, context):
    current = request.path
    current = current.strip("/")
    context.setdefault('current', current)

def index(request):
    context = {}
    currentURL(request, context)
    #request.path gets the current URL
    return render (request, 'store/base.html', context)


def inventory(request):
    myItem = Inventory.objects.get(id=1)
    #print(myItem.__dict__)
    context = { 'cost' : myItem.cost}
    currentURL(request, context)
    return render (request, 'store/inventory.html', context)

def login(request):
    return render (request, 'store/login.html')

def get_services(request):
	result_set = []

#will we only use this for "order" views?
#@login_required(login_url='login')

def about(request):
    context = {}
    currentURL(request, context)
    return render(request, 'store/about.html')

def Items(request):
    """
    # figure out who is logged in.
    user = request.user
    user_profile = UserProfile.objects.get(user=user.id)
    department_id = user_profile.department.id
    department_ids = [dept.id for dept in user_profile.alt_departments.all()]
    department_ids.append(department_id)
"""
    Items = Inventory.objects.get(id=1)
    context = {'Items' : Items}
    # render them in a list.
    return render(request, 'store/Inventory.html')
    #, { 'Item': inventory_text,
        #'sorting': sort_urls,
        #'sort_arrows': sort_arrows
    #}, context=RequestContext(request))

## from nameform

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'store/name.html', {'form': form})
    result_set = []
