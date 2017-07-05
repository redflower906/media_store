from django.shortcuts import render, get_object_or_404
from django.template import context
## from nameform 
from .forms import NameForm, item_model_formset_factory, NumInput
from django.http import HttpResponseRedirect
from .models import Inventory
import MySQLdb, sys
#from django.http import HttpResponse
'''
NOT WORKING
def current_URL(request, context):
    current = request.path
    print(current)
    current = current.strip("/")
    context.setdefault('current', current)
'''

def index(request):
    context = {}
    #current_URL(request, context)
    #request.path gets the current URL
    return render (request, 'store/home.html', context)

def home(request):
    context = {}
    #current_URL(request, context)
    return render(request, 'store/home.html', context)

def login(request):
    return render (request, 'store/login.html')

def get_items(request):
	result_set = []

#will we only use this for "order" views?
#@login_required(login_url='login')


def services(request):
    context = {}
    #current_URL(request, context)
    return render(request, 'store/about.html')

def add_item(request):
    context = {}
    #current_URL(request, context)
    return render(request, 'store/add_item.html')


def inventory(request):
    """
    # figure out who is logged in.
    user = request.user
    user_profile = UserProfile.objects.get(user=user.id)
    department_id = user_profile.department.id
    department_ids = [dept.id for dept in user_profile.alt_departments.all()]
    department_ids.append(department_id)
"""
    context = {}
    #current_URL(request, context)
    InventoryItems = Inventory.objects.all()
    #sort
    Items = InventoryItems.order_by('inventory_text')
    sort_urls = {'name': '?o=name', 'department': '?o=department'}
    sort_arrows = {}
    # render them in a list.
    return render(request, 
        'store/inventory.html', 
        {
        'InventoryItems' : InventoryItems
        }, context)

#@login_required(login_url='login')
def create_item(request):
    ItemModelFormset = item_model_formset_factory(extra=2)
    item = Inventory.objects.values_list('id', flat=True)
    formset = ItemModelFormset()
    print(item[0])
    '''
    If usr select item pk exists, then go to item(id) page
    else to to item_form
    '''
    #what does if request.method == "post" do???
    #from what I read, POST is used for form submissions that affect the database. So do we even
    #need the if? Nevermind, the if is to process the submitted form, otherwise it just returns
    #the blank form.
    if request.method == "POST":
        formset = ItemModelFormset(request.POST)
        # create item
        if formset.is_valid():
            formset.save()
            messages.success(request, 
            'item {0} was successfully created.'.format(item.name))
            return HttpResponseRedirect('/item/{0}'.format(item.id))

    # just show the form
    return render(request, 
    'store/item_form.html', {
        'formset': formset
        }, context)
def single_item(request, id):
    if request.method == "POST":
        return _update_item(request, id)
    elif request.method == "DELETE":
        return _delete_item(request, id)
    else:
        return _get_item(request, id)
'''
#is this necessary? shouldn't I just use edit single item?
def _update_item(request, id):
    SingleItem = get_object_or_404(Inventory, pk=id)
    ItemModelFormSet = item_model_formset_factory()
    return render(request, 
    'store/item_form.html', {
        'formset': formset
        }, context)
'''

def _delete_item(request, id):
    SingleItem = get_object_or_404(Inventory, pk=id)

    #can't delete an item that's associated with an order

    if item.order_set.count() > 0:
        return HttpResponseBadRequest(simplejson.dumps({'failed': 'This item is still associated with existing orders and cant be deleted. Please mark it as inactive instead'}), content_type="application/json")
    item.delete()
    return HttpResponse(simplejson.dumps({'deleted': id}), content_type="application/json")

        
    # from nameform
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
